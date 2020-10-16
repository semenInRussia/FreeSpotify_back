from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.publicFeatures import get_tracks_top, get_link_on_artist_img
from buisness_logic.tests.func.test_rocknationAPI import spotify, artist_name
from buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_track_top

artist_name = 'ac dc'

spotify = Spotify()


def testGetTracksTop():
    top = get_tracks_top(artist_name, spotify=spotify)

    _assert_is_public_track_top(top)


def _assert_is_public_track_top(top: list):
    _assert_is_track_top(top)

    assert top[0].get("album_link")
    assert top[0].get("artist_link")
    assert top[0].get("album_img_link")


def test_get_link_on_artist_img__by_artist_name():
    link = get_link_on_artist_img(spotify=spotify, artist_name=artist_name)

    assert link == "https://rocknation.su/upload/images/bands/1.jpg"
