import sys
from argparse import ArgumentParser, Namespace

import pytest

from commands.simple_commands.cli_command import CLICommand
from commands.simple_commands_collections.cli_commands_collection import CLICommandsCollection
from server.main import app
from settings import main
from settings import server
from ui.bot_programm import TelegramUI
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

    def run(self, args: list):
        console_ui = ConsoleUI()
        console_ui.run()


class RunBotCommand(CLICommand):
    aliases = ['bot', 'run-bot']

    def run(self, args: list, additional_settings=None, **kwargs):
        ui = TelegramUI(additional_settings)
        ui.run()


class RunTestsCommand(CLICommand):
    aliases = ['tests', 'run-tests', 'runtests', 'pytest', 'test']

    def run(self, args: list):
        sys.exit(pytest.main(['..']))


class MainCLICommandsCollection(CLICommandsCollection):
    all_commands = [
        RunServerCommand(),
        RunConsoleUICommand(),
        RunTestsCommand(),
        RunBotCommand(),
    ]
