from loguru import logger

from spotify import Spotify


class SaveSpotifyObjectMixIn:
    def _save_spotify(self, *args, **kwargs):
        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()
