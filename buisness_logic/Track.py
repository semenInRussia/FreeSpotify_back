class BaseTrack:
    def __init__(self, artist_name: str, album_name: str, track_name: str, top_number: int = None,
                 disc_number: int = None, release_date: str = None):
        self._artist_name = artist_name
        self._album_name = album_name
        self._track_name = track_name
        self._disc_number = disc_number
        self._top_number = top_number
        self._release_date = release_date


class Track(BaseTrack):
    pass
