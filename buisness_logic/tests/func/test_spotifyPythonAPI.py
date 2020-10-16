from backend.buisness_logic.SpotifyWebAPI.features import Spotify
from backend.buisness_logic.spotifyPythonAPI import get_artists_ids_and_names, get_top_music_info, \
    get_top_music_info_by_approximate_artist_title

spotify = Spotify()

ac_dc_spotify_id = '711MCceyCBcFnzjGY4Q7Un'

artist_name = 'AC/DC'
album_name = 'back in black'
track_name = 'back in black'
release_year = '1980'


def testGetArtistsIdsAndNames():
    artists_ids_and_names = get_artists_ids_and_names('ac dc', spotify=spotify)

    assert (len(artists_ids_and_names) == 1)
    assert (artists_ids_and_names[0]['artist_title'] == 'AC/DC')
    assert (artists_ids_and_names[0]['artist_id'] == ac_dc_spotify_id)


def testGetTopMusicInfo():
    top = get_top_music_info(ac_dc_spotify_id, spotify)

    _assert_is_track_top(top)

def testGetTopMusicInfoByApproximateArtistTitle():
    top_music_info = get_top_music_info_by_approximate_artist_title(artist_name, spotify=spotify)

    assert(len(top_music_info) == 10)

def _assert_is_track_top(top: list) -> None:
    assert top is not None
    assert isinstance(top, list)
    assert len(top) == 10

    assert top[0].get("artist_name")
    assert top[0].get("name")
    assert top[0].get("album_name")
    assert top[0].get("album_name")
    assert top[0].get("top_number")
    assert top[0].get("disc_number")
    assert top[0].get("release_date")
