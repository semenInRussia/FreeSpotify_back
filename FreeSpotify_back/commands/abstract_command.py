class Command:
    """The abstract class defines methods of an executable command.

    This command can be either called only in the some cases or in all.
    """

    aliases: list[str] = []

    def run(self, *args, **kwargs) -> None:
        """Run the command.

        This method doesn't check can be the command called, you should ensure
        that it's true
        """
        pass

    def is_selected(self, *args) -> bool:
        """Determine can command be called or not.

        The default behavior is check `self.aliases` if one of given arguments
        is one of them then return true.
        """
        return self.get_selected_alias(*args) in self.aliases

    def get_selected_alias(self, alias: str) -> str:
        """Determine a given alias is an alias of the command or not.

        By default just check with ==
        """
        return alias
