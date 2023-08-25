MAIN_PAGE_URL = "/api/"

template_for_url = MAIN_PAGE_URL + "{url}/"


ARTISTS_WELCOME_PAGE_URL = template_for_url.format(url="artists")

ARTIST_DETAIL_PAGE_URL = template_for_url.format(url="artists/detail/<artist_name>")

ALBUMS_WELCOME_PAGE_URL = template_for_url.format(url="albums")

ALBUM_DETAIL_PAGE_URL = template_for_url.format(
    url="albums/detail/<artist_name>/<name>"
)

TRACKS_WELCOME_PAGE_URL = template_for_url.format(url="tracks")

TRACK_DETAIL_PAGE_URL = template_for_url.format(
    url="tracks/detail/<artist_name>/<album_name>/<name>"
)
