from typing import NamedTuple


class TrackDto(NamedTuple):
    artist_name: str
    album_name: str
    name: str

    disc_number: int = None

    def __repr__(self):
        return f"{self.artist_name} - {self.disc_number}.{self.name}"


class AlbumDto(NamedTuple):
    artist_name: str
    name: str

    release_date: str = None

    spotify_id: str = None

    def __repr__(self):
        return f"{self.artist_name} - {self.name}"


class ArtistDto(NamedTuple):
    name: str
    spotify_id: str = None

    def __repr__(self):
        return self.name
