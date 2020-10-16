from django.http import JsonResponse

# Create your views here.
from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.publicFeatures import get_tracks_top

spotify = Spotify()


def view_artist_detail(request, artist_name: str):
    top = get_tracks_top(artist_name, spotify=spotify)
    track = top[0]
    precise_artist_name = track["artist_name"]

    return JsonResponse({
        "top": top,
        "name": precise_artist_name,
        "img_link": ""
    })
