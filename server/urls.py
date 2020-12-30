MAIN_PAGE_URL = '/api/'

template_for_url = MAIN_PAGE_URL + "{url}/"

ARTISTS_URL = template_for_url.format(url='artists')

ARTIST_DETAIL_URL = template_for_url.format(url='artists/detail/<artist_name>')

ALBUMS_URL = template_for_url.format(url='albums')

ALBUM_DETAIL_URL = template_for_url.format(url='albums/detail/<artist_name>/<name>')

TRACKS_URL = template_for_url.format(url='tracks')

TRACK_DETAIL_URL = template_for_url.format(url='tracks/detail/<artist_name>/<album_name>/<name>')
