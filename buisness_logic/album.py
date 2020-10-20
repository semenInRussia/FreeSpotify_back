class BaseAlbum:
    def __init__(self, artist_name: str, album_name: str, spotify_id: str = None):
        self._artist_name = artist_name
        self._album_name = album_name
        self._spotify_id = spotify_id

class Album(BaseAlbum):
    @property
    def name(self):
        return self._album_name

