from argparse import ArgumentParser

from FreeSpotify_back.commands import CLICommand, CLICommandsCollection
from FreeSpotify_back.server.handlers import app
from FreeSpotify_back.settings.main import main
from FreeSpotify_back.settings.server import server
from FreeSpotify_back.ui.console_ui import ConsoleUI
from FreeSpotify_back.ui.tg_bot import TelegramUI


class RunServerCommand(CLICommand):
    """Command-line command to start the REST-api server of `FreeSpotify_back`.

    To start use one of aliases (see `self.aliases`) in command line arguments,
    these arguments can be provided into this class via `run` method
    """

    aliases = ["server", "run-server", "runserver", "rest-api"]

    @property
    def parser(self) -> ArgumentParser:
        """Parser of command-line arguments."""
        server_parser = ArgumentParser()

        server_parser.add_argument(
            "-p",
            "--port",
            "-P",
            type=int,
            help=main.help_text_for_port,
            default=server.PORT,
        )

        return server_parser

    def run(self, args: list[str]) -> None:
        """Run the command with given command-line arguments."""
        namespace = self.parser.parse_args(args)
        port = namespace.port

        app.run(host=server.HOST, port=port)


class RunConsoleUICommand(CLICommand):
    """Command-line command to start the REST-api shell of `FreeSpotify_back`.

    To start use one of aliases (see `self.aliases`) in command line arguments,
    these arguments can be provided into this class via `run` method
    """

    aliases = ["console", "cli-api", "shell"]

    def run(self, _args: list[str]) -> None:
        """Run the command with given command-line arguments."""
        console_ui = ConsoleUI()
        console_ui.run()


class RunBotCommand(CLICommand):
    """Command-line command to start the telegram bot of `FreeSpotify_back`.

    To start use one of aliases (see `self.aliases`) in command line arguments,
    these arguments can be provided into this class via `run` method
    """

    aliases = ["bot", "run-bot"]

    def run(self, _args: list[str], additional_settings=None, **kwargs) -> None:
        """Run the command with given command line arguments and settings of the bot."""
        telegram_ui = TelegramUI(additional_settings)
        telegram_ui.run()


class MainCLICommandsCollection(CLICommandsCollection):
    """A class-runner of command line interface for `FreeSpotify_back`."""

    all_commands = [
        RunServerCommand(),
        RunConsoleUICommand(),
        RunBotCommand(),
    ]
