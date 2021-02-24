import os
from typing import List

import similarity_lib
from dto import AlbumDto, ArtistDto, TrackDto
from music_manger.implementations.DirectoryMusicManager._directory_artists_manager import DirectoryArtistsManager
from music_manger.music_manger import AbstractAlbums, AbstractArtists


RATIO_OF_SIMILARITY_OF_ALBUMS = 0.5

class DirectoryAlbumsManager(AbstractAlbums):
    def __init__(self, path_to_music: str):
        self._path = path_to_music

    def search(self, artist_name: str, album_name: str) -> List[AlbumDto]:
        current_album = AlbumDto(artist_name, album_name)

        similar_albums = self._get_albums_similar_to(current_album)

        return similar_albums

    def _get_albums_similar_to(self, album: AlbumDto) -> List[AlbumDto]:
        all_albums = self._get_all_albums()
        filtered_and_sorted_by_similarity_albums = self._filtered_and_sorted_albums_by_similarity_to(album, all_albums)

        return filtered_and_sorted_by_similarity_albums

    def _get_all_albums(self) -> List[AlbumDto]:
        all_artists = self._get_all_artists()
        all_albums = self._get_albums_by_artists(all_artists)

        return all_albums

    def _get_all_artists(self) -> List[ArtistDto]:
        artist_names = self._get_all_artists_names()
        artists = self._get_artists_by_names(artist_names)

        return artists

    def _get_all_artists_names(self) -> List[str]:
        return os.listdir(self._path)

    def _get_artists_by_names(self, artist_names: List[str]) -> List[ArtistDto]:
        return list(map(
            ArtistDto,

            artist_names
        ))

    def _get_albums_by_artists(self, artists: List[ArtistDto]) -> List[AlbumDto]:
        albums = []

        for artist in artists:
            artist_albums = self._get_albums_by_artist(artist)
            albums.extend(artist_albums)

        return albums

    def _get_albums_by_artist(self, artist: ArtistDto) -> List[AlbumDto]:
        path_to_artist = self._get_path_to_artist(artist)
        albums = self._get_albums_by_path_to_artist(path_to_artist)

        return albums

    def _get_path_to_artist(self, artist: ArtistDto) -> str:
        real_artist = self._artists.get(artist.name)

        return os.path.join(self._path, real_artist.name)

    def _get_albums_by_path_to_artist(self, path_to_artist: str) -> List[AlbumDto]:
        albums_names = self._get_albums_names_by_path_to_artist(path_to_artist)

        artist = self._get_artist_by_path(path_to_artist)

        albums = self._get_albums_by_names_and_artist(albums_names, artist)

        return albums

    def _get_albums_names_by_path_to_artist(self, path_to_artist: str) -> List[str]:
        return os.listdir(path_to_artist)

    def _get_albums_by_names_and_artist(self, albums_names: List[str], artist: ArtistDto) -> List[AlbumDto]:
        return list(map(
            lambda album_name: AlbumDto(artist.name, album_name),

            albums_names
        ))

    def _get_artist_by_path(self, path_to_artist: str) -> ArtistDto:
        artist_name = self._get_artist_name_by_path(path_to_artist)

        return ArtistDto(artist_name)

    def _get_artist_name_by_path(self, path_to_artist: str) -> str:
        return os.path.basename(path_to_artist)

    def _filtered_and_sorted_albums_by_similarity_to(self, album: AlbumDto, albums: List[AlbumDto]) -> List[AlbumDto]:
        filtered_albums = self._filtered_albums_by_min_similarity_to(album, albums)
        filtered_and_sorted_albums = self._sorted_albums_by_similarity_to(album, filtered_albums)

        return filtered_and_sorted_albums

    def _filtered_albums_by_min_similarity_to(self, album: AlbumDto, albums: List[AlbumDto]) -> List[AlbumDto]:
        return list(filter(
            lambda current_album: self._is_similar_albums(album, current_album),

            albums
        ))

    def _sorted_albums_by_similarity_to(self, album: AlbumDto, albums: List[AlbumDto]) -> List[AlbumDto]:
        return list(sorted(
            albums,

            key=lambda current_album: -(self._get_ratio_of_similarity_albums(album, current_album))
        ))

    def _is_similar_albums(self, actual_album: AlbumDto, expected_album: AlbumDto) -> bool:
        return similarity_lib.is_similar_strings(
            str(actual_album),
            str(expected_album),

            RATIO_OF_SIMILARITY_OF_ALBUMS
        )

    def _get_ratio_of_similarity_albums(self, actual_album: AlbumDto, expected_album: AlbumDto) -> float:
        return similarity_lib.get_ratio_of_similarity(
            str(actual_album),
            str(expected_album)
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

    @property
    def _artists(self) -> AbstractArtists:
        return DirectoryArtistsManager(self._path)
