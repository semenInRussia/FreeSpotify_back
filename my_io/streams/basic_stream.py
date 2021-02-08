from my_io.abstract_stream import AbstractStream


class BasicStream(AbstractStream):
    def listen(self, answer) -> object:
        return answer

    def write(self, content="\n", *args, **kwargs):
        super().write(content, *args, **kwargs)
