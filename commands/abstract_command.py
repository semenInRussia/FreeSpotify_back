class Command:
    aliases: list = []

    @staticmethod
    def run(self):
        # There are run code logic ...
        pass

    def is_selected(self, *args) -> bool:
        return self.get_selected_alias(*args) in self.aliases

    def get_selected_alias(self, alias) -> str:
        return alias
