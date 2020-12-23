from core import exceptions
from runner.cli_commands import ServerCommand, ConsoleCommand


class AbstractCommandsCollection:
    all_commands = []

    def run(self, *args, **kwargs):
        pass

    def find_command(self, *args, **kwargs):
        for command in self.all_commands:
            if command.is_selected(*args, **kwargs):
                return command

        raise exceptions.NotFoundCommandException


class CLICommandsCollection(AbstractCommandsCollection):
    all_commands = [
        ServerCommand(),
        ConsoleCommand()
    ]

    def run(self, args: list):
        command = self.find_command(args)

        command.run(args[1:])
