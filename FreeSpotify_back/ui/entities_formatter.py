from collections.abc import Iterable

from FreeSpotify_back._low_level_utils import first_true, my_format_str
from FreeSpotify_back.entities import Album, Artist, Track


class AbstractParseMode:
    """Class that defines format to print entities."""

    name: str
    artist: str
    top_item: str
    artist_header: str
    album_header: str
    album_track: str
    track: str


class TextParseMode(AbstractParseMode):
    """A common format to print entities."""

    name = "text"
    artist = """
    {artist_header}
    {top_items}
    """
    top_item = """
    {num_in_top}. {track.name}
        {track.album.name|'"Album not found..."'} ({track.album.release_date|'"Album not found..."'})
        URL (ON ALBUM):
         {track.album.link|'"Link not found..."'}

        URL (ON TRACK):
         {track.link|"'Link not found...'"}
    """
    artist_header = """
    {artist.name}
        IMG URL - {artist.link_on_img|'Not found picture...'}
        URL - {artist.link|'Not found link...'}
    """
    album_header = """
    {album.name} [{album.release_date}|3000]
        IMG URL - {album.link_on_img|'Not found picture...'}
        URL - {album.link|'Not found link...'}
    """
    album_track = """
    {track.disc_number|''}. {track.name}
       {track.link|''}
    """
    track = """
    {track.name}
        IMG: {track.link_on_img}
        ARTIST: {track.artist.name} {track.artist.link}
        ALBUM: {track.album.name} {track.album.link}
        DOWNLOAD: {track.link}
    """


class TelegramMarkdownParseMode(AbstractParseMode):
    """A telegram markdown format to print entities."""

    name = "markdown"

    artist = """
    {artist_header}
    {top_items}
    """

    artist_header = """
    {artist.name}
        [URL ON IMAGE]({artist.link_on_img|"https://i.ytimg.com/vi/96iDGkuOb3M/maxresdefault.jpg"})
        [URL ON ARTIST]({artist.link|"Not found..."})
    """

    top_item = """
    {num_in_top}. [{track.name}]({track.link|"Not found..."})
        [{track.album.name|"Not found..."}]({track.album.link|"Not found..."}) - {track.album.release_date|"Not found..."}
    """

    album_header = """
    {album.name} ({album.release_date|3000})
        [[IMG URL]({album.link_on_img|'Not found picture...'})]
        [[URL]({album.link|'Not found link...'})]
    """

    album_track = "{track.disc_number| }. [{track.name}]({track.link})\n"
    track = """
    {track.artist.name} - {track.name} ({track.album.release_year|3000})
      [IMG]({track.link_on_img|''})
      [{track.artist.name}]({track.artist.link|''})
      [{track.album.name}]({track.album.link|''})
      [DOWNLOAD]({track.link|''})
    """


def get_parse_mode_by_name(parse_mode_name: str) -> AbstractParseMode:
    """Return the format to print entities with a given name."""
    parse_mode = first_true(all_parse_modes,
        pred=lambda pm: pm.name == parse_mode_name)

    if not parse_mode:
       raise KeyError(f"Not found parse mode with name: {parse_mode_name}")

    return parse_mode


all_parse_modes: Iterable[AbstractParseMode] = [
    TextParseMode(),
    TelegramMarkdownParseMode(),
]


def format_artist(artist: Artist, parse_mode: AbstractParseMode) -> str:
    """Return an artist in a given string format."""
    artist_header = _format_artist_to_header(artist, parse_mode)
    top_items = format_top_items(artist.top, parse_mode)

    return my_format_str(
        parse_mode.artist,
        top_items=top_items,
        artist_header=artist_header,
    )


def format_top_items(top: Iterable[Track],
                     parse_mode: AbstractParseMode) -> str:
    """Return a artist top in a given string format."""
    res = ""

    for n, track in enumerate(top):
        res += format_top_item(track, n + 1, parse_mode)

    return res


def format_top_item(track: Track,
                    num_in_top: int,
                    parse_mode: AbstractParseMode) -> str:
    """Return an artist top item in a given string format."""
    return my_format_str(
        parse_mode.top_item,
        num_in_top=num_in_top,
        track=track,
    )


def _format_artist_to_header(artist: Artist,
                             parse_mode: AbstractParseMode) -> str:
    return my_format_str(
        parse_mode.artist_header,
        artist=artist,
    )


def format_album(album: Album, parse_mode: AbstractParseMode) -> str:
    """Return an album in a given string format."""
    header = _format_album_to_header(album, parse_mode)
    tracks = _format_album_tracks(album.tracks, parse_mode)
    return header + "\n" + tracks


def _format_album_to_header(album: Album,
                            parse_mode: AbstractParseMode) -> str:
    return my_format_str(parse_mode.album_header, album=album)


def _format_album_tracks(tracks: Iterable[Track],
                         parse_mode: AbstractParseMode) -> str:
    return "".join(my_format_str(parse_mode.album_track, track=t) for t in tracks)

def format_track(track: Track, parse_mode: AbstractParseMode) -> str:
    """Return a track in a given string format."""
    return my_format_str(parse_mode.track,
                         track=track)
