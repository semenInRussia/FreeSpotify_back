from dto import ArtistDto
from entities._AbstractEntity import AbstractEntity
from music_manger.core.exceptions import NotFoundArtistException


class Artist(AbstractEntity):

    def __init__(self, artist_name: str, additional_settings=None):
        self._init_settings(additional_settings)
        self._init_instance(artist_name)

        super().__init__(additional_settings=additional_settings)

    def _init_instance(self, artist_name):
        self._instance = ArtistDto(
            name=artist_name
        )
        self._update_instance()

    def _update_instance(self):
        self._instance = self._music_mgr.artists.get(self.name)

    def __repr__(self):
        return repr(self._instance)

    @property
    def name(self) -> str:
        return self._instance.name

    @property
    def top(self):
        track_dto_top = self._music_mgr.artists.get_top(self.name)

        track_top = self._get_top_from_dto_top(track_dto_top)

        return track_top

    def _get_top_from_dto_top(self, track_dto_top):
        from entities.track import Track

        top = []

        for dto_track in track_dto_top:
            track = Track.create_from_dto(dto_track, additional_settings=self.settings)

            top.append(track)

        return top

    @property
    def link(self):
        try:
            return self._music_mgr.artists.get_link(
                self._instance.name
            )
        except NotFoundArtistException:
            return

    @property
    def link_on_img(self):
        try:
            return self._music_mgr.artists.get_link_on_img(
                self.name
            )
        except NotFoundArtistException:
            return None

    @classmethod
    def create_from_dto(cls, dto: ArtistDto, additional_settings=None):
        return cls(
            dto.name,

            additional_settings=additional_settings
        )
