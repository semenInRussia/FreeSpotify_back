import sys

from .main_cli_commands import MainCLICommandsCollection

commands = MainCLICommandsCollection()


def run() -> None:
    """Run the `FreeSpotify_back` application with provided from the user arguments."""
    commands.run(sys.argv[1:])


if __name__ == "__main__":
    run()
