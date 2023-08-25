class InvalidJsonResponseError(Exception):
    template_of_exception_msg = "Response from the url ({url}) contains invalid JSON."

    def __init__(self, url: str):
        self.txt = self.template_of_exception_msg.format(url=url)

        super().__init__(url)


class UndefinedCommandError(Exception):
    """A given command isn't defined."""


class InvalidFormatExpressionError(Exception):
    """By use `_low_level_utils.my_format_str` not found `FormatExpression`."""
