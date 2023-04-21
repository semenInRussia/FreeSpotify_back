from collections.abc import Callable
from typing import Optional

from FreeSpotify_back.entities import Album, Artist, Track

from .entities_formatter import (
    AbstractParseMode,
    format_album,
    format_artist,
    format_track,
    get_parse_mode_by_name,
)
from .handler_collection import HandlersCollection


class UnknownCommandError(Exception):
    """You indicated unknow command or not indicated."""

class AbstractUI:
    r"""Abstract class to define UI for multi-platform chat bot to search tracks.

    To support your special bot platform, you should:

    1.  Create the HandlersCollection class (or AsyncHandlersCollection if your UI is
        async) using wrapper `<collection>.new_handler(<method name>)`.  Using it you
        should implement the following methods (* means required method) (spaces should
        be copied precisely)

       - [*] "print normal message"
       - [*] "print error
       - [ ] "start"
       - [ ] "finish"

       They should accepet one argument: a message to print on your platform

    2a. If your UI has the architecture where exists function that can just return an
        user message if ask then just pass it to `create_ui` function (it's outside
        class' scope) together with handlers collection (see 1) and parse mode (see 3)
    2b. Otherwise, create the new class that inherits from `AbstractUI` and redefine
        `run` methods.  For example, you can do the function which bind some handlers to
        special events and run them as a bot (it's depends on python APIs for which you
        do wrapper)
    3.  Chose method to display bot responses, you can choose either "text" (for plain
        text format) or "markdown" or create your own (see `entities_formatter`)
    """

    handlers: HandlersCollection

    _parse_mode_name: str = "text"
    _parse_mode: Optional[AbstractParseMode] = None

    def __init__(self, additional_entities_settings=None):
        """Create a new object with a given settings."""
        self._additional_entities_settings = additional_entities_settings

    def run(self) -> None:
        """Start the chat bot user interface.

        If your UI gets messages from user no using function, then you can
        write your own run method (suggest visit tg_bot)
        """
        self._raise_event_or_call_self_method("start")
        self.handlers.execute_calls_queue()

        try:
            while True:
                user_message = self.get_user_message()
                try:
                    self.handle_user_message(user_message)
                except Exception as exc:
                    self.print_error(exc)

        except KeyboardInterrupt:
            self._raise_event_or_call_self_method("finish")

        self.handlers.execute_calls_queue()

    def _raise_event_or_call_self_method(self, event_name: str) -> None:
        """If handler of event is exist, then raise event.

        Otherwise run method of current class called event_name.
        """
        if self.handlers.is_has_handlers_on_events(event_name):
            self.handlers.raise_event(event_name)
        else:
            method = getattr(self, event_name)
            method()

    def get_user_message(self) -> str:
        """Read a message from the user and return it."""
        return NotImplemented

    def handle_user_message(self, msg: str) -> None:
        """Accept an user message and do anything."""
        for command in _commands:
            if command.is_run(msg):
                command.execute(msg, self)
                return
        raise UnknownCommandError

    @property
    def parse_mode(self) -> AbstractParseMode:
        """Return the parsing mode of the UI."""
        if not self._parse_mode:
            self._parse_mode = get_parse_mode_by_name(self._parse_mode_name)
        return self._parse_mode

    def print_normal_message(self, message: str) -> None:
        """Just print a message using the UI methods."""
        self.handlers.raise_event("print normal message", message)

    def print_error(self, exception: Exception) -> None:
        """Print an error message using the UI methods."""
        self.handlers.raise_event("print error", exception)

    def start(self) -> None:
        """Do things before the UI start.

        You can rewrite this method specially for your UI
        """
        self.print_normal_message("Hello, Good Luck!")

    def finish(self) -> None:
        """Do things before the UI close.

        You can rewrite this method specially for your UI
        """
        self.print_normal_message("I am leave this, GOOD BY!")


def create_ui(handlers: HandlersCollection,
              get_user_message_func: Callable[[], str],
              parse_mode_name: str = 'text'):
    """Build an abstract UI with given parameters."""
    class UI(AbstractUI):
        def __init__(self, *args, **kwargs):
            self.handlers = handlers
            self._parse_mode_name = parse_mode_name

            super().__init__(*args, **kwargs)

        @staticmethod
        def get_user_message() -> str:
            return get_user_message_func()

    return UI


class _Command:
    """Abstract class for command can be used for every AbstractUI implementation."""

    command_name: str

    def is_run(self, msg: str) -> bool:
        """If in given msg the user need to run the command, return True."""
        return msg.startswith(self._command_prefix)

    def execute(self, _msg: str, _ui: AbstractUI) -> None:
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

    def execute(self, msg: str, ui: AbstractUI) -> None:
        artist_name = msg.removeprefix(self._command_prefix).strip()
        message = self._format_artist_by_name(artist_name, ui)
        ui.print_normal_message(message)

    def _format_artist_by_name(self, artist_name: str, ui: AbstractUI) -> str:
        artist = Artist(artist_name)
        return format_artist(artist, ui.parse_mode)


class _SearchAlbumCommand(_Command):
    command_name = "album"

    def execute(self, msg: str, ui: AbstractUI) -> None:
        query = msg.removeprefix(self._command_prefix)
        album = Album.from_query(query)
        ui.print_normal_message(format_album(album, ui.parse_mode))


class _SearchTrackCommand(_Command):
    command_name = "track"

    def execute(self, msg: str, ui: AbstractUI) -> None:
        query = msg.removeprefix(self._command_prefix)
        track = Track.from_query(query)
        ui.print_normal_message(format_track(track, ui.parse_mode))


_commands: list[_Command] = [_SearchArtistCommand(),
                             _SearchAlbumCommand(),
                             _SearchTrackCommand()]
