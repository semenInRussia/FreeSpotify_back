from my_io.streams import ConsoleStream


class StreamForConsoleUI(ConsoleStream):
    def listen(self, **kwargs) -> str:
        return super().listen("Enter band's name")
