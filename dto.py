from typing import NamedTuple
from typing import Optional


class TrackDto(NamedTuple):
    artist_name: str
    album_name: str
    name: str
    disc_number: Optional[int] = None

    def __repr__(self):
        return f"{self.artist_name} - {self.disc_number}.{self.name}"


class AlbumDto(NamedTuple):
    artist_name: str
    name: str
    release_date: Optional[str] = None
    spotify_id: Optional[str] = None

    def __repr__(self):
        return f"{self.artist_name} - {self.name}"


class ArtistDto(NamedTuple):
    name: str
    spotify_id: Optional[str] = None

    def __repr__(self):
        return self.name
