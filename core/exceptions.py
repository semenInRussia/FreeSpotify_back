class NotJsonResponseFromUrl(Exception):
    template_of_exception_message = """Response from this url ({url}), not decode to JSON."""

    def __init__(self, url: str):
        self.txt = self.template_of_exception_message.format(
            url=url
        )

        super().__init__(url)

class NotFoundCommandException(Exception):
    """Your Alias Is Not Defined."""
