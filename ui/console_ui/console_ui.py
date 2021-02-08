from ui.abstract_ui import AbstractUI
from ui.console_ui.stream_for_console_ui import StreamForConsoleUI


class ConsoleUI(AbstractUI):
    stream = StreamForConsoleUI()


if __name__ == "__main__":
    stream = ConsoleUI()
    stream.run()
