from __future__ import annotations

from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing_extensions import override


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
            node_version_requirement='>=18',
        )
        context.variables.update({
            'server_directory_path': str(cls.plugin_storage_path / 'server')
        })

