from music_manger.implementations.RocknationAndSpotify.rocknation.rocknationAPI import RocknationArtists, \
    RocknationAlbums
from music_manger.implementations.RocknationAndSpotify.spotify.spotifyPythonAPI import SpotifyArtists, SpotifyAlbums, \
    SpotifyTracks
from music_manger.music_manger import AbstractMusicManager

class RocknationAndSpotifyArtists(RocknationArtists, SpotifyArtists):
    pass

class RocknationAndSpotifyAlbums(RocknationAlbums, SpotifyAlbums):
    pass

class RocknationAndSpotifyTracks(SpotifyTracks):
    pass

class RocknationAndSpotify(AbstractMusicManager):
    artists = RocknationAndSpotifyArtists()
    albums = RocknationAndSpotifyAlbums()
    tracks = RocknationAndSpotifyTracks()
