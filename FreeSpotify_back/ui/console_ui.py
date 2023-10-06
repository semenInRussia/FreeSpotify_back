from sys import stderr

from .ui import AbstractUI


class ConsoleUI(AbstractUI):
    def get_user_message(self, _state=None) -> str:
        return input("Enter: ")

    def print_normal_message(self, msg: str, _state=None) -> None:
        print(msg)

    def print_error(self, err: Exception, _state=None) -> None:
        error_name = err.__class__.__name__
        error_doc = err.__doc__
        error_description = f"Detail: {error_doc}" if error_doc else ""

        print(
            f"""Sorry!!!!\n\tError: \t{error_name}\n\tDetail: \t{error_description}""",
            file=stderr,
        )


if __name__ == "__main__":
    ConsoleUI().run()
