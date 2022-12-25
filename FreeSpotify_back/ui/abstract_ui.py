from typing import Callable
from typing import Optional

from ..entities import Artist
from ..entities import Album
from ..entities import Track

from .entities_formatter import AbstractParseMode
from .entities_formatter import format_artist
from .entities_formatter import format_album
from .entities_formatter import get_parse_mode_by_name
from .entities_formatter import format_track

from .handler_collection import HandlersCollection

class UnknownCommandException(Exception):
    """You indicated unknow command or not indicated"""

class AbstractUI:
    handlers: HandlersCollection

    _parse_mode_name: str = "text"
    _parse_mode: Optional[AbstractParseMode] = None

    def __init__(self, additional_entities_settings=None):
        self._additional_entities_settings = additional_entities_settings

    def run(self):
        # if your UI gets messages from user no using function, then you can
        # write your own run method (suggest visit tg_bot)
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

    def _raise_event_or_call_self_method(self, event_name: str):
        """
        If has handler on event, then raise event,
        Otherwise run method of current class called event_name
        """
        if self.handlers.is_has_handlers_on_events(event_name):
            self.handlers.raise_event(event_name)
        else:
            method = getattr(self, event_name)
            method()

    def get_user_message(self) -> str:
        return NotImplemented

    def handle_user_message(self, msg: str):
        for command in _commands:
            if command.is_run(msg):
                command.execute(msg, self)
                return
        raise UnknownCommandException
    @property
    def parse_mode(self):
        if not self._parse_mode:
            self._parse_mode = get_parse_mode_by_name(self._parse_mode_name)

        return self._parse_mode

    def print_normal_message(self, message: str):
        self.handlers.raise_event("print normal message", message)

    def print_error(self, exception: Exception):
        self.handlers.raise_event("print error", exception)

    def start(self):
        self.print_normal_message("Hello, Good Luck!")

    def finish(self):
        self.print_normal_message("I am leave this, GOOD BY!")


def create_ui(handlers: HandlersCollection,
              get_user_message_func: Callable[[], str],
              parse_mode_name: str = 'text'):
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
    command_name: str

    def is_run(self, msg: str) -> bool:
        """
        If in given msg user need to run this command, return True,
        otherwise False
        """
        return msg.startswith(self._command_prefix)

    def execute(self, _msg: str, _ui: AbstractUI):
        """
        Execute this command, using preferences written in given msg
        and methods of object AbstractUI
        """
        return NotImplemented

    @property
    def _command_prefix(self):
        return "/" + self.command_name

class _SearchArtistCommand(_Command):
    command_name = "artist"
    _ui: AbstractUI

    def execute(self, msg: str, ui: AbstractUI):
        artist_name = msg.removeprefix(self._command_prefix).strip()
        message = self._format_artist_by_name(artist_name, ui)
        ui.print_normal_message(message)

    def _format_artist_by_name(self, artist_name: str, ui: AbstractUI) -> str:
        artist = Artist(artist_name)
        return format_artist(artist, ui.parse_mode)


class _SearchAlbumCommand(_Command):
    command_name = "album"

    def execute(self, msg: str, ui: AbstractUI):
        query = msg.removeprefix(self._command_prefix)
        album = Album.from_query(query)
        ui.print_normal_message(format_album(album, ui.parse_mode))


class _SearchTrackCommand(_Command):
    command_name = "track"

    def execute(self, msg: str, ui: AbstractUI):
        query = msg.removeprefix(self._command_prefix)
        track = Track.from_query(query)
        ui.print_normal_message(format_track(track, ui.parse_mode))


_commands: list[_Command] = [_SearchArtistCommand(),
                             _SearchAlbumCommand(),
                             _SearchTrackCommand()]
