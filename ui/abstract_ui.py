import traceback
from typing import Callable

from entities import Artist
from entities_formatter import AbstractParseMode
from entities_formatter import format_artist
from entities_formatter import get_parse_mode_by_name
from ui.handler_collection import HandlersCollection


class AbstractUI:
    handlers: HandlersCollection

    _parse_mode_name: str = "text"
    _parse_mode: AbstractParseMode = None

    def __init__(self, additional_entities_settings=None):
        self._additional_entities_settings = additional_entities_settings

    def run(self):
        self._raise_event_or_call_self_method("start")

        self.handlers.execute_calls_queue()

        try:
            while True:
                user_message = self.get_user_message()

                self.print_artist(user_message)
                self.handlers.execute_calls_queue()

        except KeyboardInterrupt:
            self._raise_event_or_call_self_method("finish")

        self.handlers.execute_calls_queue()

    def _raise_event_or_call_self_method(self, event_name: str):
        """
        If has handler on event -> raise event,
        Else -> run method of current class with '_' + event_name
        """

        if self.handlers.is_has_handlers_on_events(event_name):
            self.handlers.raise_event(event_name)

        else:
            method_name = '_' + event_name
            method = getattr(self, method_name)

            method()

    def get_user_message(self) -> str:
        """Implement if you control getting user message."""

    def print_artist(self, artist_name: str):
        try:
            message = self._format_artist_by_name(artist_name)

        except Exception as e:
            self._print_error(e)

        else:
            self._print_normal_message(message)

    def _format_artist_by_name(self, artist_name: str) -> str:
        artist = Artist(artist_name)

        return format_artist(artist, self.parse_mode)

    @property
    def parse_mode(self):
        if not self._parse_mode:
            self._parse_mode = get_parse_mode_by_name(self._parse_mode_name)

        return self._parse_mode

    def _print_normal_message(self, message: str):
        self.handlers.raise_event("print normal message", message)

    def _print_error(self, exception: Exception):
        traceback.print_exc()

        self.handlers.raise_event("print error", exception)

    def _start(self):
        self._print_normal_message("Hello, Good Luck!")

    def _finish(self):
        self._print_normal_message("I am leave this, GOOD BY!")


def create_ui(handlers: HandlersCollection, get_user_message_func: Callable, parse_mode_name: str = 'text'):
    class UI(AbstractUI):
        def __init__(self, *args, **kwargs):
            self.handlers = handlers
            self._parse_mode_name = parse_mode_name

            super().__init__(*args, **kwargs)

    UI.get_user_message = staticmethod(get_user_message_func)

    return UI
