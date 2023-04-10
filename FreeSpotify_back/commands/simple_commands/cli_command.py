from FreeSpotify_back.commands import Command


class CLICommand(Command):
    """Abstract class for a command line command."""

    def run(self, args: list[str]) -> None:
        """Run a command that matched with command line arguments."""
        pass

    def get_selected_alias(self, args: list[str]) -> str:
        """Return a command name or alias from given command line arguments."""
        try:
            return args[0]
        except IndexError:
            raise AttributeError('Not inputted command name.') from IndexError
