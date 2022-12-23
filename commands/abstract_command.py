import abc

class Command(abc.ABC):
    aliases: list = []

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def is_selected(self, *args) -> bool:
        return self.get_selected_alias(*args) in self.aliases

    @abc.abstractmethod
    def get_selected_alias(self, alias) -> str:
        return alias
