from argparse import ArgumentParser, Namespace

import console_gui
from server.main import app
from settings.general import help_text_for_port
from settings.server import PORT, HOST


class Command:
    aliases: list = []

    @staticmethod
    def run(self):
        # There are run code logic ...
        pass

    def is_selected(self, *args, **kwargs) -> bool:
        if self.get_selected_alias(*args, **kwargs) in self.aliases:
            return True

        return False

    def get_selected_alias(self, *args, **kwargs) -> str:
        pass


class CLICommand(Command):
    def get_selected_alias(self, args: list) -> str:
        try:
            return args[0]
        except IndexError:
            raise AttributeError('You input not valid data. Not inputted command name.')

class ServerCommand(CLICommand):
    aliases = ['server', 'rest-api']

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
    aliases = ['console', 'cli-api']

    def run(self, args: list):
        console_gui.run()



