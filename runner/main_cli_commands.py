import sys
from argparse import ArgumentParser, Namespace

import pytest

import console_gui

from commands.commands import CLICommand
from commands.commands_collections import CLICommandsCollection

from server.main import app

from settings import main
from settings import server


class ServerCommand(CLICommand):
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


class ConsoleCommand(CLICommand):
    aliases = ['console', 'cli-api', 'shell']

    def run(self, args: list):
        console_gui.run()


class RunTestsCommand(CLICommand):
    aliases = ['tests', 'run-tests', 'runtests', 'pytest', 'test']

    def run(self, args: list):
        sys.exit(pytest.main(['..']))


class RunBotCommand(CLICommand):
    aliases = ['bot', 'run-bot']

    def run(self, *args, **kwargs):
        from bot.main import run

        run()


class MainCLICommandsCollection(CLICommandsCollection):
    all_commands = [
        ServerCommand(),
        ConsoleCommand(),
        RunTestsCommand(),
        RunBotCommand(),
    ]
