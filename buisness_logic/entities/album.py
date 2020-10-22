from typing import NamedTuple

from buisness_logic.entities._base import BaseEntityMixIn


class BaseAlbum(BaseEntityMixIn, NamedTuple):
    artist_name: str
    album_name: str

    def __str__(self):
        return f"{self.artist_name} - {self.album_name}"

    def __repr__(self):
        return self.__str__()


class Album(BaseAlbum):
    @property
    def artist(self):
        from buisness_logic.entities.artist import Artist

        return Artist(self.artist_name)

    @property
    def name(self):
        return self.album_name
