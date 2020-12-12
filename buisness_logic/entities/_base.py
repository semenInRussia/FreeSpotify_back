from loguru import logger

from buisness_logic.spotify.spotifyPythonAPI import Spotify


class SaveSpotifyObjectMixIn:
    def _save_spotify(self, *args, **kwargs):
        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()
