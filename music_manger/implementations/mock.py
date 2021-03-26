import random
from typing import List

from dto import AlbumDto, ArtistDto, TrackDto
from music_manger.music_manger import AbstractMusicManager, AbstractAlbums, AbstractArtists, AbstractTracks

def _create_random_name():
    names = ["I AM DIED?", "Me and dog: forever", "Gob vs Devil", "!!!SUpEr CoOl!!!",
             "My crazy cats!", "I am eat my T_SHORT", "Please, kill me!?",
             "I am your FATHER \\0_0/", "Basic", "IV White Album", "III White Album",
             "We are the gobs: I", "We are the gobs: II"]

    return random.choice(names)

class MockAlbums(AbstractAlbums):
    def search(self, artist_name: str, album_name: str, limit: int = 4) -> List[AlbumDto]:
        return [
            AlbumDto(
                artist_name=artist_name,
                name=_create_random_name(),
                release_date='2020-14-12',
            ) for _ in range(limit)
        ]

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                name=_create_random_name(),
                artist_name=artist_name,
                album_name=album_name
            ) for _ in range(random.randint(6, 21))
        ]

    def get_link(self, artist_name, album_name: str) -> str:
        return f"https://rocknation.su/mp3/album-{random.randint(1, 2500)}"

    def get_link_on_img(self, artist_name: str, album_name: str) -> str:
        return f"https://rocknation.su/upload/images/albums/{random.randint(1, 2500)}.jpg"


class MockArtists(AbstractArtists):
    def search(self, artist_name: str, limit: int = 3) -> List[ArtistDto]:
        return [
            ArtistDto(
                name=_create_random_name()
            ) for _ in range(limit)
        ]

    def get_top(self, artist_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                name=_create_random_name() + str(i),
                artist_name=artist_name,
                album_name=_create_random_name()
            ) for i in range(10)
        ]

    def get_link(self, artist_name: str) -> str:
        return f"https://rocknation.su/mp3/band-{random.randint(1, 266)}"

    def get_link_on_img(self, artist_name: str) -> str:
        return f"https://rocknation.su/upload/images/bands/{random.randint(1, 266)}.jpg"


class MockTracks(AbstractTracks):
    def search(self, artist_name: str, track_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                artist_name=artist_name,
                album_name=_create_random_name(),
                name=track_name,
                disc_number=111
            ) for _ in range(3)
        ]

    def get_link(self, artist_name: str, album_name: str, track_name: str) -> str:
        return ""

    def get_link_on_img(self, artist_name: str, album_name: str, track_name: str) -> str:
        return f"https://rocknation.su/upload/images/albums/{random.randint(1, 1500)}.jpg"


class MockMusicManager(AbstractMusicManager):
    artists = MockArtists()
    albums = MockAlbums()
    tracks = MockTracks()
