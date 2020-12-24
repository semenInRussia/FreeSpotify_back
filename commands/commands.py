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

    def is_selected(self, *args) -> bool:
        if self.get_selected_alias(*args) in self.aliases:
            return True

        return False

    def get_selected_alias(self, alias) -> str:
        return alias


class CLICommand(Command):
    def get_selected_alias(self, args: list) -> str:
        try:
            return args[0]
        except IndexError:
            raise AttributeError('Not inputted command name.')
