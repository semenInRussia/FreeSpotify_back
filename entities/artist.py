from dto import ArtistDto
from entities._mixins import _Entity


class Artist(_Entity):

    def __init__(self, artist_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._init_instance(artist_name)

    def _init_instance(self, artist_name):
        self._instance = ArtistDto(
            name=artist_name
        )
        self._update_instance()

    def _update_instance(self):
        self._instance = self._music_mgr.artists.get(self.name)

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
            track = Track.create_from_dto(dto_track)

            top.append(track)

        return top

    @property
    def link(self):
        return self._music_mgr.artists.get_link(
            self._instance.name
        )

    @property
    def link_on_img(self):
        return self._music_mgr.artists.get_link_on_img(
            self.name
        )

    @classmethod
    def create_from_dto(cls, dto):
        return cls(
            dto.name
        )
