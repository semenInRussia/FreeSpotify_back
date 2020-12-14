from loguru import logger

from music_manger.implementations.RocknationAndSpotify.spotify import Spotify


class SaveSpotifyObjectMixIn:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()
