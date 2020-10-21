from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.spotifyPythonAPI import get_artists_ids_and_names, get_top_music_info, \
    get_top_music_info_by_approximate_artist_title, get_tracks_info, search_albums_by_spotify_id, search_albums

spotify = Spotify()

ac_dc_spotify_id = '711MCceyCBcFnzjGY4Q7Un'

artist_name = 'AC/DC'
album_spotify_id = '6mUdeDZCsExyJLMdAfDuwh'
album_name = 'back in black'
track_name = 'back in black'
release_year = '1980'


def testGetArtistsIdsAndNames():
    artists_ids_and_names = get_artists_ids_and_names('ac dc', spotify=spotify)

    assert (len(artists_ids_and_names) == 1)
    assert (artists_ids_and_names[0].artist.name == 'AC/DC')
    assert (artists_ids_and_names[0].artist.spotify_id == ac_dc_spotify_id)

def testGetTopMusicInfo():
    top = get_top_music_info(ac_dc_spotify_id, spotify)

    _assert_is_track_top(top)

def test_get_tracks_info():
    data = get_tracks_info("Ac dc - T.N.T", spotify=spotify)

    first_artist = data[0]

    # assert is valid tracks info
    _assert_is_valid_track_info(first_artist)

def testGetTopMusicInfoByApproximateArtistTitle():
    top_music_info = get_top_music_info_by_approximate_artist_title(artist_name, spotify=spotify)

    assert(len(top_music_info) == 10)

def _assert_is_valid_track_info(track_info):
    assert track_info.album.release_date
    assert track_info.name
    assert track_info.allbum_name
    assert track_info.artist.name

def _assert_is_track_top(top: list) -> None:
    assert top is not None
    assert isinstance(top, list)
    assert len(top) == 10

    assert top[0].artist.name
    assert top[0].name
    assert top[0].album.name
    assert top[0].disc_number
    assert top[0].album.release_date

def test_albums_info():
    albums = search_albums_by_spotify_id(album_spotify_id, spotify=spotify)
    album = albums[0]

    assert album.name
    assert album.artist.name
    assert album.spotify_id

def test_search_albums():
    albums = search_albums(artist_name, spotify=spotify)
    album = albums[-1]

    assert isinstance(albums, list), "search_albums() must return type - list"
    assert album.name
    assert album.artist.name
