from FreeSpotify_back.entities import Album, Artist, Track

from .entities_formatter import (
    AbstractParseMode,
    TextParseMode,
    format_album,
    format_artist,
    format_track,
    get_parse_mode_by_name,
)


class UnknownCommandError(Exception):
    """You indicated unknow command or not indicated."""


class AbstractUI:
    """Abstract class to define user multiplatform interfaces.

    Here the UI is a chat-like interface."""

    _parse_mode_name: str = "text"
    _parse_mode: AbstractParseMode = TextParseMode()

    def __init__(self, additional_entities_settings=None):
        self._additional_entities_settings = additional_entities_settings

    def run(self) -> None:
        """Start the application.

        If your UI gets messages from user no using function, then you can
        write your own run method (suggest visit tg_bot)"""
        self.start()

        try:
            while True:
                user_message = self.get_user_message()
                try:
                    self.handle_user_message(user_message)
                except Exception as exc:
                    self.print_error(exc)

        except KeyboardInterrupt:
            self.finish()

    def start(self, _state=None) -> None:
        """A code which will be executed before app is run.

        It's not required to implement and accept a state.  You can use some other
        abstract methods inside it."""
        pass

    def get_user_message(self, _state=None) -> str:
        """Return a message readed from an user.

        In the most of apps this method is hard to implement, if it's true
        then just redefine the method `run`."""
        return NotImplemented

    def handle_user_message(self, msg: str, state=None) -> None:
        """Accept an user message and do anything..

        This is the main function of this abstract method and how I
        think shouldn't be redefined.

        Here some abstract functions are used."""
        for command in _commands:
            if command.is_run(msg, state):
                command.execute(msg, self, state)
                return
        raise UnknownCommandError

    def print_normal_message(self, _msg: str, _state=None) -> None:
        """Print a normal message using state."""
        pass

    def print_error(self, err: Exception, _state=None) -> None:
        """Tell to user that an error is occured.

        The default behaviour is just print error description and name
        as a normal message."""
        error_name = err.__class__.__name__
        error_doc = err.__doc__
        error_description = f"Detail: {error_doc}" if error_doc else ""

        self.print_normal_message(
            f"""Sorry!!!!
Error: {error_name}
Detail: {error_description}""",
        )

    def finish(self, _state=None) -> None:
        """Do things before the UI close."""

        pass

    @property
    def parse_mode(self) -> AbstractParseMode:
        """Return the parsing mode of the UI."""
        if not self._parse_mode:
            self._parse_mode = get_parse_mode_by_name(self._parse_mode_name)
        return self._parse_mode



class _Command:
    """Abstract class for command can be used for every AbstractUI implementation."""

    command_name: str

    def is_run(self, msg: str, _state=None) -> bool:
        """If in given msg the user need to run the command, return True."""
        return msg.startswith(self._command_prefix)

    def execute(self, _msg: str, _ui: AbstractUI, _state=None) -> None:
        r"""Execute this command, using preferences written in given msg.

        This method MUST be redefined

        To print a message use the `ui.print_normal_message()` method also see
        `AbstractUI` to see full list of abilities.

        """
        return

    @property
    def _command_prefix(self) -> str:
        return "/" + self.command_name


class _SearchArtistCommand(_Command):
    command_name = "artist"
    _ui: AbstractUI

    def execute(self, msg: str, ui: AbstractUI, _state=None) -> None:
        artist_name = msg.removeprefix(self._command_prefix).strip()
        message = self._format_artist_by_name(artist_name, ui)
        ui.print_normal_message(message)

    def _format_artist_by_name(self, artist_name: str, ui: AbstractUI) -> str:
        artist = Artist(artist_name)
        return format_artist(artist, ui.parse_mode)


class _SearchAlbumCommand(_Command):
    command_name = "album"

    def execute(self, msg: str, ui: AbstractUI, _state=None) -> None:
        query = msg.removeprefix(self._command_prefix)
        album = Album.from_query(query)
        ui.print_normal_message(format_album(album, ui.parse_mode))


class _SearchTrackCommand(_Command):
    command_name = "track"

    def execute(self, msg: str, ui: AbstractUI, _state=None) -> None:
        query = msg.removeprefix(self._command_prefix)
        track = Track.from_query(query)
        ui.print_normal_message(format_track(track, ui.parse_mode))


_commands: list[_Command] = [
    _SearchArtistCommand(),
    _SearchAlbumCommand(),
    _SearchTrackCommand(),
]
