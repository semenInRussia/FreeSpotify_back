from FreeSpotify_back.music_manager import AbstractMusicManager  # noqa: N999
from FreeSpotify_back.settings.entities import entities


class AbstractEntity:
    def __init__(
        self,
        additional_settings=None,  # noqa: ANN001
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ):
        self._init_settings(additional_settings)

        super().__init__(*args, **kwargs)

    @property
    def settings(self):  # noqa: ANN202
        return self.__settings

    def _init_settings(self, additional_settings) -> None:  # noqa: ANN202
        self.__settings = entities
        self.__settings += additional_settings

    @property
    def _music_mgr(self) -> AbstractMusicManager:
        return self.settings.music_manager_impl()
