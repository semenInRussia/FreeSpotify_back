from typing import NamedTuple, Optional


class ArtistDto(NamedTuple):
    """Object that represent a music artist in the most simple form."""

    name: str
    spotify_id: Optional[str] = None

    def __repr__(self):
        return self.name

class AlbumDto(NamedTuple):
    """Object that represent a music album in the most simple form."""

    artist_name: str
    name: str
    release_date: Optional[str] = None
    spotify_id: Optional[str] = None

    def __repr__(self):
        return f"{self.artist_name} - {self.name}"


class TrackDto(NamedTuple):
    """Object that represent a music track in the most simple form."""

    artist_name: str
    album_name: str
    name: str
    disc_number: Optional[int] = None

    def __repr__(self):
        return f"{self.artist_name} - {self.disc_number}.{self.name}"
