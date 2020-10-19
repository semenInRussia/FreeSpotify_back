class Artist:
    def __init__(self, artist_name: str):
        self._artist_name = artist_name

    @property
    def name(self):
        return self._artist_name
