class BaseAlbum:
    def __init__(self, artist_name: str, album_name: str, spotify_id: str = None):
        self._artist_name = artist_name
        self._album_name = album_name
        self.spotify_id = spotify_id

class Album(BaseAlbum):
    @property
    def artist(self):
        from buisness_logic.artist import Artist

        return Artist(self._artist_name)

    @property
    def name(self):
        return self._album_name

