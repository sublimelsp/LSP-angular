import os
from lsp_utils import NpmClientHandler


def plugin_loaded():
    LspAngularPlugin.setup()


def plugin_unloaded():
    LspAngularPlugin.cleanup()


class LspAngularPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = "server"
    server_binary_path = os.path.join(server_directory, "node_modules", "@angular", "language-server", "index.js")
