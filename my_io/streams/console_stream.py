from my_io.abstract_stream import AbstractStream


class ConsoleStream(AbstractStream):
    def write(self, content="\n", *args, **kwargs):
        print(content, *args, **kwargs)

        super().write(content, *args, **kwargs)

    def listen(self, prompt: str = "") -> str:
        return input(prompt)

    def stop(self, *args, **kwargs):
        self.write("By!")

    @property
    def is_stop(self) -> bool:
        return False
