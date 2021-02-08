from loguru import logger

from entities import Artist, Track
from my_io.abstract_stream import AbstractStream
from ui.statuses import Status, Statuses


class AbstractUI:
    stream: AbstractStream = None
    status: Status = Status()

    def __init__(self, additional_settings=None):
        self._additional_settings = additional_settings

    def print_artist(self, artist_name: str):
        logger.debug(f"print_artist - OK, artist_name={artist_name}")

        self.stream.write(
            self.get_string_artist(artist_name)
        )

        logger.debug(f"artist printed successfully!")

    def get_string_artist(self, artist_name: str) -> str:
        try:
            return self._try_get_string_artist(artist_name)
        except Exception as e:
            return self._raise_and_format_exception(e)

    def _raise_and_format_exception(self, exception: Exception) -> str:
        self.status.set(Statuses.FAIL)

        return self._format_exception(exception)

    @staticmethod
    def _format_exception(exception: Exception) -> str:
        exception_name = exception.__class__.__name__
        formatted_exception_name = f"Name: {exception_name}"

        exception_description = exception.__class__.__doc__
        formatted_exception_description = f"Description: {exception_description}\n" if exception_description else ""

        return (
            f"{formatted_exception_name}\n"
            f"{formatted_exception_description}"
        )

    def _try_get_string_artist(self, artist_name: str) -> str:
        logger.info(f"get artist - OK, artist_name={artist_name}")

        artist = Artist(artist_name, additional_settings=self._additional_settings)
        top = artist.top

        res = ""
        res += self._get_string_artist_info_by_artist(artist)
        res += self._get_string_artist_top(top)

        return res

    def _get_string_artist_top(self, top) -> str:
        result = ""

        for i, track in enumerate(top):
            result += self._get_string_top_item(i, track)

        return result

    @staticmethod
    def _get_string_top_item(index, track: Track) -> str:
        logger.info(f"get top item - OK, index={index}; track={track}")
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
        logger.info(f"get top - OK, artist={artist}")
        return (
            f"{artist.name}\n"
            f"    IMG URL - {artist.link_on_img}\n"
            f"    URL - {artist.link}\n"
            "\n"
        )

    def by(self):
        logger.info("by - OK")

        self.stream.write()
        self.stream.write("By, I am Master, you are not master!")
        self.stream.write()

    def run(self):
        try:
            while not self.stream.is_stop:
                self.print_artist(
                    str(self.stream.listen())
                )
        except KeyboardInterrupt:
            self.by()
