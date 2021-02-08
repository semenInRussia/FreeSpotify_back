class AbstractStream:
    result: str = ""
    last_result: str = ""

    def listen(self, *args, **kwargs) -> object:
        return ""

    def write(self, content=None, *args, **kwargs):
        self._update_results(content)

    def _update_results(self, content):
        self.last_result = content

        self.result += str(content)
        self.result += "\n"

    @property
    def is_stop(self) -> bool:
        return True

    def stop(self, *args, **kwargs):
        pass
