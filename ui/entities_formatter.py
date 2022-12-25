from typing import Iterable

from FreeSpotify_back._low_level_utils import my_format_str
from FreeSpotify_back.entities import Album
from FreeSpotify_back.entities import Artist
from FreeSpotify_back.entities import Track


class AbstractParseMode:
    name: str
    artist_template: str
    top_item_template: str
    artist_header_template: str
    album_header_template: str
    album_track: str
    track: str


class TextParseMode(AbstractParseMode):
    name = "text"
    artist_template = """
    {artist_header}
    {top_items}
    """
    top_item_template = """
    {num_in_top}. {track.name}
        {track.album.name|'"Album not found..."'} ({track.album.release_date|'"Album not found..."'})
        URL (ON ALBUM):
         {track.album.link|'"Link not found..."'}

        URL (ON TRACK):
         {track.link|"'Link not found...'"}
    """
    artist_header_template = """
    {artist.name}
        IMG URL - {artist.link_on_img|Not found picture...}
        URL - {artist.link|Not found link...}
    """
    album_header_template = """
    {album.name} [{album.release_date}|3000]
        IMG URL - {album.link_on_img|Not found picture...}
        URL - {album.link|Not found link...}
    """
    album_track = """
    {track.disc_number| }. {track.name}
       {track.link}
    """
    track = """
    {track.name}
        IMG: {track.link_on_img}
        ALBUM: {track.album.name}
        DOWNLOAD: {track.link}
    """


class TelegramMarkdownParseMode(AbstractParseMode):
    name = "markdown"

    artist_template = """
    {artist_header}
    {top_items}
    """

    artist_header_template = """
    {artist.name}
        [URL ON IMAGE]({artist.link_on_img|"https://i.ytimg.com/vi/96iDGkuOb3M/maxresdefault.jpg"})
        [URL ON ARTIST]({artist.link|"Not found..."})
    """

    top_item_template = """
    {num_in_top}. [{track.name}]({track.link|"Not found..."})
        [{track.album.name|"Not found..."}]({track.album.link|"Not found..."}) - {track.album.release_date|"Not found..."}
    """

    album_header_template = """
    {album.name} ({album.release_date}|3000)
        [[IMG URL]({album.link_on_img|Not found picture...})]
        [[URL]({album.link|Not found link...})]
    """

    album_track = "{track.disc_number| }. [[{track.name}]({track.link})]\n"
    track = """
    {track.name}
        [[IMG]({track.link_on_img})]
        [[ALBUM]({track.album.name})]
        [[DOWNLOAD]({track.link})]
    """


def get_parse_mode_by_name(parse_mode_name: str) -> AbstractParseMode:
    for actual_parse_mode in all_parse_modes:
        if actual_parse_mode.name == parse_mode_name:
            return actual_parse_mode
    raise KeyError(f"Not found parse mode with name: {parse_mode_name}")


all_parse_modes: Iterable[AbstractParseMode] = [
    TextParseMode(),
    TelegramMarkdownParseMode()
]


def format_artist(artist: Artist, parse_mode: AbstractParseMode) -> str:
    artist_header = format_artist_to_header(artist, parse_mode)
    top_items = format_top_items(artist.top, parse_mode)

    return my_format_str(
        parse_mode.artist_template,

        top_items=top_items,
        artist_header=artist_header
    )


def format_top_items(top: Iterable[Track],
                     parse_mode: AbstractParseMode) -> str:
    res = ""

    for n, track in enumerate(top):
        res += format_top_item(track, n + 1, parse_mode)

    return res


def format_top_item(track: Track,
                    num_in_top: int,
                    parse_mode: AbstractParseMode) -> str:
    return my_format_str(
        parse_mode.top_item_template,

        num_in_top=num_in_top,
        track=track
    )


def format_artist_to_header(artist: Artist,
                            parse_mode: AbstractParseMode) -> str:
    return my_format_str(
        parse_mode.artist_header_template,
        artist=artist
    )


def format_album(album: Album, parse_mode: AbstractParseMode) -> str:
    header = format_album_to_header(album, parse_mode)
    tracks = format_album_tracks(album.tracks, parse_mode)
    return header + "\n" + tracks


def format_album_to_header(album: Album,
                           parse_mode: AbstractParseMode) -> str:
    return my_format_str(parse_mode.album_header_template, album=album)


def format_album_tracks(tracks: Iterable[Track],
                        parse_mode: AbstractParseMode) -> str:
    return "".join(map(
        lambda t: my_format_str(parse_mode.album_track, track=t),
        tracks))
