from loguru import logger

from music_manger.implementations.RocknationAndSpotify.spotify import Spotify


class SaveSpotifyObjectMixIn:
    def _save_spotify(self, *args, **kwargs):
        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()
