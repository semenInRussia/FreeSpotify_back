from FreeSpotify_back.music_manager import AbstractMusicManager

from .rocknation import RocknationAlbums, RocknationArtists, RocknationTracks
from .spotify.spotify import SpotifyAlbums, SpotifyArtists, SpotifyTracks


class RocknationAndSpotifyArtists(RocknationArtists, SpotifyArtists):
    pass


class RocknationAndSpotifyAlbums(RocknationAlbums, SpotifyAlbums):
    pass


class RocknationAndSpotifyTracks(RocknationTracks, SpotifyTracks):
    pass


class RocknationAndSpotify(AbstractMusicManager):
    artists = RocknationAndSpotifyArtists()
    albums = RocknationAndSpotifyAlbums()
    tracks = RocknationAndSpotifyTracks()
