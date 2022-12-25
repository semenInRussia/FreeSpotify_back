import pytest

from ..settigs_for_test import settings_with_mock

from FreeSpotify_back.dto import TrackDto
from FreeSpotify_back.entities import Album
from FreeSpotify_back.entities import Artist
from FreeSpotify_back.entities.track import Track

artist_name = "Metallica"
album_name = "Master of Puppets"
track_name = "Master of Puppets"

approximate_track_name = "master of puppet"

difference_artist_name = "Airbourne"
difference_album_name = "... And Justice For All"
difference_track_name = "Battery"

additional_settings = settings_with_mock


@pytest.fixture()
def track():
    return Track(
        artist_name=artist_name,
        album_name=album_name,
        track_name=approximate_track_name,
        additional_settings=additional_settings
    )


@pytest.fixture()
def track_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name=track_name
    )
    return track_dto


@pytest.fixture()
def not_valid_track_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name="kdkdkdkkdkdkd"
    )
    return track_dto


def test_track_artist(track):
    assert isinstance(track.artist, Artist)


def test_track_link(track):
    assert isinstance(track.link, str)


def test_work_with_settings(track):
    assert track.settings.music_manager_impl == settings_with_mock.music_manager_impl


def test_equal_tracks():
    first_track = Track(artist_name, album_name, track_name, additional_settings=additional_settings)
    second_track = Track(artist_name, album_name, track_name, additional_settings=additional_settings)

    assert first_track.name == second_track.name
    assert first_track.album == second_track.album

    assert first_track == second_track


def test_notequal_by_artists_tracks():
    first_track = Track(artist_name, album_name, track_name, additional_settings=additional_settings)
    second_track = Track(difference_artist_name, album_name, track_name, additional_settings=additional_settings)

    assert first_track != second_track


def test_notequal_by_albums_tracks():
    first_track = Track(artist_name, album_name, track_name, additional_settings=additional_settings)
    second_track = Track(artist_name, difference_album_name, track_name, additional_settings=additional_settings)

    assert first_track.album != second_track.album

    assert first_track != second_track


def test_notequal_by_names_tracks():
    first_track = Track(artist_name, album_name, track_name, additional_settings=additional_settings)
    second_track = Track(artist_name, album_name, difference_track_name, additional_settings=additional_settings)

    assert first_track != second_track


def test_notequal_with_other_types():
    assert Track(artist_name, album_name, track_name, additional_settings=additional_settings) != 0
    assert Track(artist_name, album_name, track_name, additional_settings=additional_settings) != "STRING"


def test_track_album(track):
    assert isinstance(track.album, Album)


def test_track_get_name(track):
    assert isinstance(track.name, str)


def test_track_get_disc_number(track: Track):
    assert isinstance(track.disc_number, int)


def test_track_create_from_dto(track_dto: TrackDto):
    track = Track.create_from_dto(track_dto, additional_settings=additional_settings)

    assert isinstance(track, Track)


def test_work_with_settings_when_create_from_dto(track_dto: TrackDto):
    track = Track.create_from_dto(track_dto,
        additional_settings=settings_with_mock)

    assert settings_with_mock.music_manager_impl == track.settings.music_manager_impl


def test_track_query_and_search():
    query_res = Track.query("Kanye West - power")
    search_res = Track.search("Kanye West", "Mr Fantasy", "Power")

    assert all(map(lambda obj: isinstance(obj, Track), query_res))
    assert all(map(lambda obj: isinstance(obj, Track), search_res))


def test_track_from_query():
    track = Track.from_query("Kanye West - power")

    assert isinstance(track, Track)
