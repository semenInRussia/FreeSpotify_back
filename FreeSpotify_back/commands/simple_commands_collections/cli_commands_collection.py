from .. import CommandsCollection


class CLICommandsCollection(CommandsCollection):
    def run(self, args: list[str]):
        command = self.find_command(args)
        command.run(args[1:])
