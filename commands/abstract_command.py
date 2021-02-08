class Command:
    aliases: list = []

    @staticmethod
    def run(self):
        # There are run code logic ...
        pass

    def is_selected(self, *args) -> bool:
        if self.get_selected_alias(*args) in self.aliases:
            return True

        return False

    def get_selected_alias(self, alias) -> str:
        return alias