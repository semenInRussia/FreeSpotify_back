from core import exceptions

class CommandsCollection:
    all_commands = []

    def run(self, *args, **kwargs):
        pass

    def find_command(self, *args, **kwargs):
        for command in self.all_commands:
            if command.is_selected(*args, **kwargs):
                return command

        raise exceptions.NotFoundCommandException


