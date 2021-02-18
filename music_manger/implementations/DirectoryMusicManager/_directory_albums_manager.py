import os
from typing import List

import similarity_lib
from dto import AlbumDto, ArtistDto, TrackDto
from music_manger.implementations.DirectoryMusicManager._directory_artists_manager import DirectoryArtistsManager
from music_manger.music_manger import AbstractAlbums, AbstractArtists


class DirectoryAlbumsManager(AbstractAlbums):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

    @property
    def _artists(self) -> AbstractArtists:
        return DirectoryArtistsManager(self._path)

    def search(self, artist_name: str, album_name: str) -> List[AlbumDto]:
        artist = self._get_artist(artist_name)

        albums = self._get_similar_albums_by_name_and_artist(album_name, artist)

        return albums

    def _get_artist(self, artist_name: str) -> ArtistDto:
        return self._artists.get(artist_name)

    def _get_similar_albums_by_name_and_artist(self, album_name: str, artist: ArtistDto) -> List[AlbumDto]:
        similar_albums_names = self._get_albums_names_of_artist_similar_to(album_name, artist)

        albums = self._get_albums_by_names(similar_albums_names, artist)

        return albums

    def _get_albums_names_of_artist_similar_to(self, album_name: str, artist: ArtistDto) -> List[str]:
        all_albums_names = self._get_all_albums_names_by_artist(artist)

        albums_names_simple_to_name = similarity_lib.filter_and_sort_strings_by_min_similarity_to(
            album_name,
            all_albums_names
        )

        return albums_names_simple_to_name

    def _get_all_albums_names_by_artist(self, artist: ArtistDto) -> List[str]:
        path_to_artist = self._get_path_to_artist(artist)
        all_albums_names = self._get_all_albums_names_by_path_to_artist(path_to_artist)

        return all_albums_names

    def _get_path_to_artist(self, artist: ArtistDto) -> str:
        return os.path.join(self._path, artist.name)

    def _get_all_albums_names_by_path_to_artist(self, path_to_artist: str) -> List[str]:
        for _, all_albums_names, _ in os.walk(path_to_artist):
            return all_albums_names

    def _get_albums_by_names(self, albums_names: List[str], artist: ArtistDto) -> List[AlbumDto]:
        return list(
            map(
                lambda album_name: AlbumDto(artist.name, album_name),

                albums_names
            )
        )

    def get_tracks(self, artist_name: str, album_name: str) -> List[TrackDto]:
        album = AlbumDto(artist_name, album_name)

        path_to_album = self._get_path_to_album(artist_name, album_name)
        tracks = self._get_tracks_by_path_to_album_and_album_dto(path_to_album, album)

        return tracks

    def _get_path_to_album(self, artist_name: str, album_name: str) -> str:
        album = self.get(artist_name, album_name)
        path_to_album = self._get_path_to_album_by_dto(album)

        return path_to_album

    def _get_path_to_album_by_dto(self, album: AlbumDto) -> str:
        artist = ArtistDto(album.artist_name)
        path_to_artist = self._get_path_to_artist(artist)

        path_to_album = self._get_path_to_album_by_dto_and_path_to_artist(album, path_to_artist)

        return path_to_album

    def _get_path_to_album_by_dto_and_path_to_artist(self, album: AlbumDto, path_to_artist: str) -> str:
        return os.path.join(path_to_artist, album.name)

    def _get_tracks_by_path_to_album_and_album_dto(self, path_to_album: str, album: AlbumDto) -> List[TrackDto]:
        tracks_names = self._get_tracks_names_by_path_to_album(path_to_album)
        tracks = self._get_tracks_by_tracks_names_and_dto(tracks_names, album)

        return tracks

    def _get_tracks_names_by_path_to_album(self, path_to_album: str) -> List[str]:
        for _, tracks_names, _ in os.walk(path_to_album):
            return tracks_names

    def _get_tracks_by_tracks_names_and_dto(self, tracks_names: List[str], album: AlbumDto) -> List[TrackDto]:
        return list(
            map(
                lambda track_name: TrackDto(album.artist_name, album.name, track_name),

                tracks_names
            )
        )
