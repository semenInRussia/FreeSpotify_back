from .. import Command


class CLICommand(Command):
    def run(args: list[str]):
        pass

    def get_selected_alias(self, args: list[str]) -> str:
        try:
            return args[0]
        except IndexError:
            raise AttributeError('Not inputted command name.')
