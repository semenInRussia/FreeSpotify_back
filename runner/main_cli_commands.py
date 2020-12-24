from argparse import ArgumentParser, Namespace

import console_gui
from commands.commands import CLICommand
from commands.commands_collections import CLICommandsCollection
from server.main import app
from settings.general import help_text_for_port
from settings.server import PORT, HOST

import pytest


class ServerCommand(CLICommand):
    aliases = ['server', 'run-server', 'runserver', 'rest-api']

    @property
    def parser(self):
        server_parser = ArgumentParser()

        server_parser.add_argument('-p', '--port', '-P', type=int,
                                   help=help_text_for_port,
                                   default=PORT)

        return server_parser

    def run(self, args: list):
        namespace: Namespace = self.parser.parse_args(args)

        port = namespace.port

        app.run(host=HOST,
                port=port)


class ConsoleCommand(CLICommand):
    aliases = ['console', 'cli-api', 'shell']

    def run(self, args: list):
        console_gui.run()

class RunTestsCommand(CLICommand):
    aliases = ['tests', 'run-tests', 'runtests', 'pytest']

    def run(self, args: list):
        pytest.main(['..'])


class MainCLICommandsCollection(CLICommandsCollection):
    all_commands = [
        ServerCommand(),
        ConsoleCommand(),
        RunTestsCommand()
    ]
