from loguru import logger

from settings import entities


class AbstractEntity:
    def __init__(self, additional_settings=None, *args, **kwargs):
        self._init_settings(additional_settings)

        super().__init__(*args, **kwargs)

    @property
    def settings(self):
        return self.__settings

    def _init_settings(self, additional_settings):

        self.__settings = entities
        self.__settings += additional_settings

        logger.debug(self.__settings.data)

    @property
    def _music_mgr(self):
        return self.settings.music_manager_impl()
