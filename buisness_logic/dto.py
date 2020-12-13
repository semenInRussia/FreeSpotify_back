from typing import NamedTuple


class TrackDto(NamedTuple):
    name: str
    artist_name: str
    album_name: str

    release_date: str = None
    disc_number: int = None
    top_number: int = None

    def __str__(self):
        return f"{self.artist_name} - {self.disc_number}.{self.name}"

    def __repr__(self):
        return self.__str__()


class AlbumDto(NamedTuple):
    artist_name: str
    name: str

    release_date: str = None

    spotify_id: str = None

    def __str__(self):
        return f"{self.artist_name} - {self.name}"

    def __repr__(self):
        return self.__str__()


class ArtistDto(NamedTuple):
    name: str
    spotify_id: str = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

