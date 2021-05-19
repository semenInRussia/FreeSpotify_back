from commands.abstract_commands_collections import CommandsCollection


class CLICommandsCollection(CommandsCollection):

    def run(self, args: list):
        command = self.find_command(args)

        command.run(args[1:])
