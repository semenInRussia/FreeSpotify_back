class Command:
    aliases: list[str] = []

    def run(self, *args, **kwargs):
        pass

    def is_selected(self, *args) -> bool:
        return self.get_selected_alias(*args) in self.aliases

    def get_selected_alias(self, alias) -> str:
        return alias
