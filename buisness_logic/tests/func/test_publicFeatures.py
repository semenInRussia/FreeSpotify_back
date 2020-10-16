from backend.buisness_logic.SpotifyWebAPI.features import Spotify
from backend.buisness_logic.publicFeatures import get_tracks_top
from backend.buisness_logic.tests.func.test_spotifyPythonAPI import _assert_is_track_top

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
