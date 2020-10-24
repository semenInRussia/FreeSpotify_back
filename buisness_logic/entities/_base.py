from loguru import logger

from buisness_logic.spotify.spotifyPythonAPI import Spotify


class SaveSpotifyObjectMixIn:
    def __init__(self, *args, **kwargs):
        logger.debug("BaseEntityMixIn called...")
        self._spotify = Spotify()

        super(SaveSpotifyObjectMixIn, self).__init__(args, kwargs)
