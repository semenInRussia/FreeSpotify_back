import random
from typing import List

from FreeSpotify_back.dto import AlbumDto
from FreeSpotify_back.dto import ArtistDto
from FreeSpotify_back.dto import TrackDto
from .. import AbstractAlbums
from .. import AbstractArtists
from .. import AbstractMusicManager
from .. import AbstractTracks

SEED = 1000


def _create_random_name():
    names = [
        "I AM DIED?", "Me and dog: forever", "Gob vs Devil", "!!!SUpEr CoOl!!!",
        "My crazy cats!", "I am eat my T_SHORT", "Please, kill me!?",
        "I am your FATHER \\0_0/", "Basic", "IV White Album", "III White Album",
        "We are the gobs: I", "We are the gobs: II"
    ]

    return random.choice(names)


def _create_random_disc_number():
    return random.randint(1, 77)


class MockArtists(AbstractArtists):
    def search(self, artist_name: str, limit: int = 3) -> List[ArtistDto]:
        random.seed(SEED)

        res = [
            ArtistDto(
                name=_create_random_name()
            ) for _ in range(limit)
        ]
        res[0] = ArtistDto(artist_name)

        return res

    def get_top(self, artist_name: str) -> List[TrackDto]:
        random.seed(SEED)

        return [
            TrackDto(
                name=_create_random_name() + str(i),
                artist_name=artist_name,
                album_name=_create_random_name()
            ) for i in range(10)
        ]

    def get_link(self, artist_name: str) -> str:
        random.seed(SEED)

        return f"https://rocknation.su/mp3/band-{random.randint(1, 266)}"

    def get_albums(self, artist_name: str) -> List[AlbumDto]:
        random.seed(SEED)

        return [
            AlbumDto(
                artist_name=artist_name,
                name=_create_random_name(),

                release_date="25-4-2021"
            )
        ]

    def get_link_on_img(self, artist_name: str) -> str:
        random.seed(SEED)

        return f"https://rocknation.su/upload/images/bands/{random.randint(1, 266)}.jpg"


class MockAlbums(AbstractAlbums):
    def search(
            self,
            artist_name: str,
            album_name: str,
            limit: int = 4
    ) -> List[AlbumDto]:
        random.seed(SEED)

        return [
            AlbumDto(
                artist_name=artist_name,
                name=album_name,
                release_date='2020-14-12',
            ) for _ in range(limit)
        ]

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        random.seed(SEED)

        return [
            TrackDto(
                name=_create_random_name(),
                artist_name=artist_name,
                album_name=album_name
            ) for _ in range(random.randint(6, 21))
        ]

    def get_link(self, artist_name, album_name: str) -> str:
        random.seed(SEED)

        return f"https://rocknation.su/mp3/album-{random.randint(1, 2500)}"

    def get_link_on_img(self, artist_name: str, album_name: str) -> str:
        random.seed(SEED)

        return f"https://rocknation.su/upload/images/albums/{random.randint(1, 2500)}.jpg"


class MockTracks(AbstractTracks):
    def search(
            self,
            artist_name: str,
            album_name: str,
            track_name: str
    ) -> List[TrackDto]:
        random.seed(SEED)

        return [
            TrackDto(
                artist_name=artist_name,
                album_name=album_name,
                name=track_name,
                disc_number=_create_random_disc_number()
            ) for _ in range(3)
        ]

    def get_link(
            self,
            artist_name: str,
            album_name: str,
            track_name: str
    ) -> str:
        return ""

    def get_link_on_img(
            self,
            artist_name: str,
            album_name: str,
            track_name: str
    ) -> str:
        random.seed(SEED)

        return f"https://rocknation.su/upload/images/albums/{random.randint(1, 1500)}.jpg"


class MockMusicManager(AbstractMusicManager):
    artists = MockArtists()
    albums = MockAlbums()
    tracks = MockTracks()
