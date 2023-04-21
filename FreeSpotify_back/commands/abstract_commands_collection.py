from FreeSpotify_back.core import exceptions

from .abstract_command import Command


class CommandsCollection(Command):
    """Abstract class that defines methods of objects of Command collection."""

    all_commands: list[Command] = []

    def run(self, *args, **kwargs) -> None:
        """Run one of the `self.all_commands`."""
        pass

    def find_command(self, *args, **kwargs) -> Command:
        """Return a command that suite to given arguments.

        Choose from `self.all_commands`.  If a command isn't found raise
        `exceptions.NotFoundCommandError`
        """
        for command in self.all_commands:
            if command.is_selected(*args, **kwargs):
                return command

        raise exceptions.UndefinedCommandError

