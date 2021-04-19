from music_manger.implementations.rocknation_and_spotify.rocknation.rocknationAPI import RocknationAlbums
from music_manger.implementations.rocknation_and_spotify.rocknation.rocknationAPI import RocknationArtists

from music_manger.implementations.rocknation_and_spotify.spotify.spotifyAPI import SpotifyAlbums
from music_manger.implementations.rocknation_and_spotify.spotify.spotifyAPI import SpotifyArtists
from music_manger.implementations.rocknation_and_spotify.spotify.spotifyAPI import SpotifyTracks

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
