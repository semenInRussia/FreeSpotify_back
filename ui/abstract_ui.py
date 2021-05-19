from typing import Callable
from typing import Tuple

from entities import Artist
from entities import Track
from ui.handler_collection import HandlersCollection


class AbstractUI:
    handlers: HandlersCollection = HandlersCollection()

    def __init__(self, additional_entities_settings=None):
        self._additional_entities_settings = additional_entities_settings

    def run(self):
        if self.handlers.is_has_handlers_on_events("start"):
            self.handlers.raise_event("start")
        else:
            self._start()

        self.handlers.execute_calls_queue()

        try:
            while True:
                user_message = self.get_user_message()
                self.print_artist(user_message)
                self.handlers.execute_calls_queue()

        except KeyboardInterrupt:
            if self.handlers.is_has_handlers_on_events("finish"):
                self.handlers.raise_event("finish")
            else:
                self._finish()

        self.handlers.execute_calls_queue()

    def get_user_message(self) -> str:
        pass

    def _print_normal_message(self, message: str):
        self.handlers.raise_event("print normal message", message)

    def print_artist(self, artist_name: str):
        try:
            message = self.get_message_about_artist(artist_name)

        except Exception as e:
            self._print_error(e)

        else:
            self._print_normal_message(message)

    def get_message_about_artist(self, artist_name: str) -> str:
        artist = Artist(artist_name, additional_settings=self._additional_entities_settings)

        res = ""

        res += self._get_string_artist_info_by_artist(artist)
        res += self._get_string_artist_top(artist.top)

        return res

    def _get_string_artist_top(self, top) -> str:
        result = ""

        for i, track in enumerate(top):
            result += self._get_string_top_item(i, track)

        return result

    @staticmethod
    def _get_string_top_item(index, track: Track) -> str:
        num_in_top = index + 1

        return (
            "\n"
            f"    {num_in_top}. {track.name} \n"
            f"        {track.album.name} ({track.album.release_date})\n"
            f"        URL - {track.album.link}"
            "\n"
        )

    @staticmethod
    def _get_string_artist_info_by_artist(artist: Artist) -> str:
        return (
            f"{artist.name}\n"
            f"    IMG URL - {artist.link_on_img}\n"
            f"    URL - {artist.link}\n"
            "\n"
        )

    def _print_error(self, exception: Exception):
        self.handlers.raise_event(
            "print error", *(self._format_exception(exception))
        )

    @staticmethod
    def _format_exception(exception: Exception) -> Tuple[str, str, Exception]:
        exception_name = exception.__class__.__name__
        exception_description = exception.__class__.__doc__

        return exception_name, exception_description, exception

    def _start(self):
        self._print_normal_message(
            "Hello, Good Luck!"
        )

    def _finish(self):
        self._print_normal_message(
            "I am leave this, GOOD BY!"
        )


def create_ui(handlers: HandlersCollection, get_user_message_func: Callable):
    class UI(AbstractUI):
        def __init__(self, *args, **kwargs):
            self.handlers = handlers

            super().__init__(*args, **kwargs)

    UI.get_user_message = staticmethod(get_user_message_func)

    return UI
