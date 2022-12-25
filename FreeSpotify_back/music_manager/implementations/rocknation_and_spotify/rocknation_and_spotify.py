from .rocknation import RocknationAlbums
from .rocknation import RocknationArtists
from .rocknation import RocknationTracks

from .spotify.spotify import SpotifyAlbums
from .spotify.spotify import SpotifyArtists
from .spotify.spotify import SpotifyTracks

from ... import AbstractMusicManager


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
