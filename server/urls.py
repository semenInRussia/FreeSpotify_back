MAIN_PAGE_URL = '/api/'

template_for_url = MAIN_PAGE_URL + "{url}/"

TRACKS_URL = template_for_url.format(url='tracks')

TRACK_DETAIL_URL = template_for_url.format(url='tracks/detail/<album_name>/<artist_name>/<name>')

ARTISTS_URL = template_for_url.format(url='artists')

ARTIST_DETAIL_URL = template_for_url.format(url='artists/detail/<artist_name>')
