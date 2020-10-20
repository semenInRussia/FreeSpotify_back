class Album:
    def __init__(self, artist_name: str, album_name: str):
        self._artist_name = artist_name
        self._album_name = album_name

    @property
    def name(self):
        return self._album_name
