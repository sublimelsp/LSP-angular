from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import notification_handler
from LSP.plugin import OnPreStartContext
from LSP.plugin import Session
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing import TypedDict
from typing_extensions import override
from weakref import ref
import sublime

SETTINGS_FILE = 'LSP-angular.sublime-settings'
STRICT_MODE_PROMPT_SETTING = 'angular.enable-strict-mode-prompt'
CLIENT_SIDE_FILE_WATCHER_PATTERNS = ['**/tsconfig.json', '**/*.ts', '**/*.html', '**/package.json']


class SuggestStrictModeParams(TypedDict):
    configFilePath: str
    message: str


def plugin_loaded():
    LspAngularPlugin.register()


def plugin_unloaded():
    LspAngularPlugin.unregister()


class LspAngularPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'server'),
            Path('node_modules', '@angular', 'language-server', 'index.js'),
            node_version_requirement='>=22.22.3',
        )
        context.variables.update({
            'server_directory_path': str(cls.plugin_storage_path / 'server')
        })
        cls._add_server_arguments(context)

    @classmethod
    def _add_server_arguments(cls, context: OnPreStartContext) -> None:
        """Pass the settings that the server reads from command line arguments only."""
        configuration = context.configuration
        settings = configuration.settings
        args: list[str] = []
        log = settings.get('angular.log')
        if log and log != 'off':
            args.extend(['--logFile', '${server_directory_path}/ngls.log', '--logVerbosity', log])
        if settings.get('angular.suggest.includeAutomaticOptionalChainCompletions'):
            args.append('--includeAutomaticOptionalChainCompletions')
        if settings.get('angular.suggest.includeCompletionsWithSnippetText'):
            args.append('--includeCompletionsWithSnippetText')
        auto_imports = settings.get('angular.suggest.autoImports')
        args.extend(['--includeCompletionsForModuleExports', 'false' if auto_imports is False else 'true'])
        if settings.get('angular.forceStrictTemplates'):
            args.append('--forceStrictTemplates')
        if suppressed_codes := settings.get('angular.suppressAngularDiagnosticCodes'):
            args.extend(['--suppressAngularDiagnosticCodes', suppressed_codes])
        if settings.get('angular.server.useClientSideFileWatcher'):
            args.append('--useClientSideFileWatcher')
            if not configuration.file_watcher.get('patterns'):
                configuration.file_watcher = {'patterns': CLIENT_SIDE_FILE_WATCHER_PATTERNS}
        configuration.command.extend(args)

    def __init__(self, weaksession: ref[Session]) -> None:
        super().__init__(weaksession)
        self._strict_mode_prompted_configs: set[str] = set()

    @notification_handler('angular/projectLoadingStart')
    def on_project_loading_start(self, params: None) -> None:
        if session := self.weaksession():
            session.set_config_status_async('initializing')

    @notification_handler('angular/projectLoadingFinish')
    def on_project_loading_finish(self, params: None) -> None:
        if session := self.weaksession():
            session.set_config_status_async('')

    @notification_handler('angular/suggestStrictMode')
    def on_suggest_strict_mode(self, params: SuggestStrictModeParams) -> None:
        session = self.weaksession()
        if not session:
            return
        settings = session.config.settings
        if settings.get(STRICT_MODE_PROMPT_SETTING) is False or settings.get('angular.forceStrictTemplates'):
            return
        config_file_path = params['configFilePath']
        if config_file_path in self._strict_mode_prompted_configs:
            return
        self._strict_mode_prompted_configs.add(config_file_path)
        window = session.window
        sublime.set_timeout(lambda: self._show_strict_mode_prompt(window, config_file_path))

    def _show_strict_mode_prompt(self, window: sublime.Window, config_file_path: str) -> None:
        result = sublime.yes_no_cancel_dialog(
            'Angular: Some language features are not available. To access all features, enable '
            '"strictTemplates" in "angularCompilerOptions" of the tsconfig file.',
            'Open tsconfig.json',
            'Do not show again',
        )
        if result == sublime.DIALOG_YES:
            window.open_file(config_file_path)
        elif result == sublime.DIALOG_NO:
            settings = sublime.load_settings(SETTINGS_FILE)
            server_settings = settings.get('settings') or {}
            server_settings[STRICT_MODE_PROMPT_SETTING] = False
            settings.set('settings', server_settings)
            sublime.save_settings(SETTINGS_FILE)
