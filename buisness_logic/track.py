from buisness_logic.album import Album

class BaseTrack:
    def __init__(self, artist_name: str, album_name: str, track_name: str, top_number: int = None,
                 disc_number: int = None, release_date: str = None):
        self._artist_name = artist_name
        self._album_name = album_name
        self._track_name = track_name
        self._disc_number = disc_number
        self._top_number = top_number
        self._release_date = release_date

    @property
    def artist(self):
        from buisness_logic.artist import Artist

        return Artist(self._artist_name)

    @property
    def album(self):
        return Album(self._artist_name, self._album_name)


class Track(BaseTrack):
    pass
