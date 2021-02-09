import sys
from argparse import ArgumentParser, Namespace

import pytest

from commands.simple_commands.cli_command import CLICommand
from commands.simple_commands_collections.cli_commands_collection import CLICommandsCollection
from server.main import app
from settings import main
from settings import server
from ui.bot_programm import BotProgram
from ui.console_ui import ConsoleUI


class RunServerCommand(CLICommand):
    aliases = ['server', 'run-server', 'runserver', 'rest-api']

    @property
    def parser(self):
        server_parser = ArgumentParser()

        server_parser.add_argument('-p', '--port', '-P', type=int,
                                   help=main.help_text_for_port,
                                   default=server.PORT)

        return server_parser

    def run(self, args: list):
        namespace: Namespace = self.parser.parse_args(args)

        port = namespace.port

        app.run(host=server.HOST,
                port=port)


class RunConsoleUICommand(CLICommand):
    aliases = ['console', 'cli-api', 'shell']

    def __init__(self):
        self.console_ui = ConsoleUI()

    def run(self, args: list):
        self.console_ui.run()


class RunTestsCommand(CLICommand):
    aliases = ['tests', 'run-tests', 'runtests', 'pytest', 'test']

    def run(self, args: list):
        sys.exit(pytest.main(['..']))


class RunBotCommand(CLICommand):
    aliases = ['bot', 'run-bot']

    def run(self, args: list, additional_settings=None, **kwargs):
        program = BotProgram(additional_settings)
        program.run()


class MainCLICommandsCollection(CLICommandsCollection):
    all_commands = [
        RunServerCommand(),
        RunConsoleUICommand(),
        RunTestsCommand(),
        RunBotCommand(),
    ]
