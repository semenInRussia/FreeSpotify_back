import sys
from argparse import ArgumentParser
from argparse import Namespace


import pytest

from ..settings.main import main
from ..settings.server import server

from ..ui.tg_bot import TelegramUI
from ..ui.console_ui import ConsoleUI

from ..commands import CLICommand
from ..commands import CLICommandsCollection
from ..server.handlers import app


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

    def run(self, _):
        console_ui = ConsoleUI()
        console_ui.run()


class RunBotCommand(CLICommand):
    aliases = ['bot', 'run-bot']

    def run(self, _, additional_settings=None, **kwargs):
        telegram_ui = TelegramUI(additional_settings)
        telegram_ui.run()


class RunTestsCommand(CLICommand):
    aliases = ['tests', 'run-tests', 'runtests', 'pytest', 'test']

    def run(self, _):
        sys.exit(pytest.main(['..']))


class MainCLICommandsCollection(CLICommandsCollection):
    all_commands = [
        RunServerCommand,
        RunConsoleUICommand,
        RunTestsCommand,
        RunBotCommand,
    ]
