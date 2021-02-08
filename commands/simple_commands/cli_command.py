from commands.abstract_command import Command


class CLICommand(Command):
    def get_selected_alias(self, args: list) -> str:
        try:
            return args[0]
        except IndexError:
            raise AttributeError('Not inputted command name.')
