import os
import sublime
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspAngularPlugin.setup()


def plugin_unloaded():
    LspAngularPlugin.cleanup()


class LspAngularPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "server"
    server_binary_path = os.path.join(server_directory, "node_modules", "@angular", "language-server", "index.js")

    @classmethod
    def get_binary_arguments(cls):
        ng_log_location = os.path.join(sublime.cache_path(), cls.package_name, cls.server_directory, "ngls.log")
        ng_probe_location = os.path.join(sublime.cache_path(), cls.package_name, cls.server_directory, "node_modules")
        return ["--logFile", ng_log_location, "--ngProbeLocations", ng_probe_location, "--tsProbeLocations", ng_probe_location, "--stdio"]

    @classmethod
    def install_in_cache(cls) -> bool:
        return False
