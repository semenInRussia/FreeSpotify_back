from .abstract_command import Command
from ..core import exceptions

class CommandsCollection:
    all_commands: list[Command] = []

    def run(self, *args, **kwargs):
        pass

    def find_command(self, *args, **kwargs):
        for command in self.all_commands:
            if command.is_selected(*args, **kwargs):
                return command

        raise exceptions.NotFoundCommandException


