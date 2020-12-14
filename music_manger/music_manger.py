from abc import ABC, abstractmethod


class _AbstractObjects:
    def get(self, *args, **kwargs):
        return self.search(*args, **kwargs)

    def search(self, *args, **kwargs):
        pass

    def get_link(self, *args, **kwargs):
        pass

    def get_img(self, *args, **kwargs):
        pass


class AbstractArtists(_AbstractObjects):
    def get_top(self, *args, **kwargs):
        pass


class AbstractAlbums(_AbstractObjects):
    @abstractmethod
    def get_tracks(self, *args, **kwargs):
        pass


class AbstractTracks(_AbstractObjects):
    pass


class AbstractMusicManager:
    artists = AbstractArtists()
    albums = AbstractAlbums()
    tracks = AbstractTracks()
