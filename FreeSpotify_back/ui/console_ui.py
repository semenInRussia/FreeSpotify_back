from sys import stderr

from .abstract_ui import create_ui
from .handler_collection import HandlersCollection

handlers_console = HandlersCollection()


def _get_user_message() -> str:
    return input("Enter: ")


@handlers_console.new_handler("print normal message")
def print_normal_message(message: str) -> None:
    print(message)


@handlers_console.new_handler("print error")
def print_error(error_name: str, error_description: str, *args) -> None:
    error_description = f"Detail: {error_description}" if error_description else ""

    print(
        f"""Sorry!!!!\n\tError: \t{error_name}\n\tDetail: \t{error_description}""",
        file=stderr,
    )


ConsoleUI = create_ui(handlers_console, _get_user_message)

if __name__ == "__main__":
    ConsoleUI().run()
