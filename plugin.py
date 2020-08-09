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
    ng_probe_location = os.path.join(sublime.cache_path(), package_name, server_directory, "node_modules")

    @classmethod
    def get_binary_arguments(cls):
        return ['--ngProbeLocations', cls.ng_probe_location, '--tsProbeLocations', cls.ng_probe_location, '--stdio']
