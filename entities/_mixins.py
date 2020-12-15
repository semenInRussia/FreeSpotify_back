from settings.general import music_manager_impl


class _Entity:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _music_mgr(self):
        return music_manager_impl()
