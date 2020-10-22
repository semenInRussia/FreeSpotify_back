from loguru import logger

from buisness_logic.SpotifyWebAPI.features import Spotify


class SaveSpotifyObjectMixIn:
    def __init__(self, *args, **kwargs):
        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()

