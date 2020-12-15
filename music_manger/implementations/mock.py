import random
from typing import List

from dto import AlbumDto, ArtistDto, TrackDto
from music_manger.music_manger import AbstractMusicManager, AbstractAlbums, AbstractArtists, AbstractTracks


class MockAlbums(AbstractAlbums):
    def search(self, artist_name: str, album_name: str, limit: int = 4) -> List[AlbumDto]:
        return [
            AlbumDto(
                artist_name=artist_name,
                name='test_name',
                release_date='2020-14-12'
            ) for _ in range(limit)
        ]

    def get(self, artist_name: str, album_name: str) -> AlbumDto:
        return self.search(artist_name, album_name)[0]

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                name=str(random.getstate()),
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
                name=artist_name
            ) for _ in range(limit)
        ]

    def get(self, artist_name: str) -> ArtistDto:
        return self.search(artist_name)[0]

    def get_top(self, artist_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                name=f"track{i}",
                artist_name=artist_name,
                album_name="Cool White Album"
            ) for i in range(10)
        ]

    def get_link(self, artist_name: str) -> str:
        return f"https://rocknation.su/mp3/band-{random.randint(1, 266)}"

    def get_link_on_img(self, artist_name: str) -> str:
        return f"https://rocknation.su/upload/images/bands/{random.randint(1, 266)}.jpg"


class MockTracks(AbstractTracks):
    def get(self, artist_name: str, track_name: str) -> TrackDto:
        return self.search(artist_name, track_name)[0]

    def search(self, artist_name: str, track_name: str) -> List[TrackDto]:
        return [
            TrackDto(
                artist_name=artist_name,
                album_name="cool white ALBUM!",
                name=track_name,
            )
        ]

    def get_link(self, artist_name: str, album_name: str, track_name: str) -> str:
        return ""

    def get_link_on_img(self, artist_name: str, album_name: str, track_name: str) -> str:
        return f"https://rocknation.su/upload/images/albums/{random.randint(1, 1500)}.jpg"


class MockMusicManager(AbstractMusicManager):
    artists = MockArtists()
    albums = MockAlbums()
    tracks = MockTracks()
