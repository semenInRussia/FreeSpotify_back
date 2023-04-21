from FreeSpotify_back.commands import CLICommand, CommandsCollection


class CLICommandsCollection(CommandsCollection):
    """Abstract class of collection of command line commands.

    This is a standard CLI-app class.
    """

    all_commands: list[CLICommand]

    def run(self, args: list[str]) -> None:
        """Run the CLI-app.

        Notice that search of choosed command will do between `self.all_commands`
        commands
        """
        command = self.find_command(args)
        command.run(args[1:])
