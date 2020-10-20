from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.spotifyPythonAPI import get_artists_ids_and_names, get_top_music_info


class Artist:
    def __init__(self, artist_name: str):
        self._spotify = Spotify()

        self._artist_name = artist_name

    @property
    def name(self):
        return self._get_artist_info()["artist_name"]

    def _get_artist_info(self) -> dict:
        artists_info = get_artists_ids_and_names(self._artist_name, self._spotify)

        return artists_info[0]

    def get_top(self):
        return get_top_music_info(self.name, spotify=self._spotify)
