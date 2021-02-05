from settings import entities


class AbstractEntity:
    def __init__(self, additional_settings=None, *args, **kwargs):
        self.__init_settings(additional_settings)

        super().__init__(*args, **kwargs)

    def __init_settings(self, additional_settings):
        self.settings = entities
        self.settings += additional_settings

    @property
    def _music_mgr(self):
        return self.settings.music_manager_impl()
