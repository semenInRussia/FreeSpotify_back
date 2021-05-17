from sys import stderr

from ui.abstract_ui import create_ui
from ui.handler_collection import HandlersCollection

handlers_console = HandlersCollection()


def _get_user_message():
    return input("Enter:")


@handlers_console.new_handler("print normal message")
def print_normal_message(message: str):
    print(message)


@handlers_console.new_handler("print error")
def print_error(message: str):
    print(message, stderr)


ConsoleUI = create_ui(handlers_console, _get_user_message)

if __name__ == '__main__':
    ConsoleUI().run()
