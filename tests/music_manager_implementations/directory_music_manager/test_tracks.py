import os

import pytest

from FreeSpotify_back.dto import TrackDto
from FreeSpotify_back.music_manager.implementations import DirectoryMusicManager
from ...testing_data import path_to_music


@pytest.fixture()
def tracks_manager():
    return DirectoryMusicManager(path=path_to_music).tracks


@pytest.fixture()
def track():
    return TrackDto(artist_name="artist1", album_name="album1", name="track1")


def test_query(tracks_manager, track: TrackDto):
    query = "artist1 - track1"
    actual = list(tracks_manager.query(query))
    assert actual[0] == track


def test_search(tracks_manager, track: TrackDto):
    actual = list(tracks_manager.search("artist1", "album1", "track1"))

    assert actual[0] == track


def test_get(tracks_manager, track: TrackDto):
    actual = tracks_manager.get("artist 1", "album  1", "track 1")

    assert actual == track


def test_get_link(tracks_manager):
    excepted = tracks_manager.get_link("artist 1", "1 album", "trakc 1")
    actual = os.path.join(path_to_music, "artist1", "album1", "track1.mp3")

    assert excepted == actual
