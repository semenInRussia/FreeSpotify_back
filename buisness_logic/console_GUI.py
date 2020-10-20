import buisness_logic
from buisness_logic.SpotifyWebAPI.features import Spotify
from buisness_logic.publicFeatures import get_tracks_top
from buisness_logic.rocknationAPI import get_link_on_artist
from buisness_logic.spotifyPythonAPI import get_artist_info

spotify = Spotify()


def main():
    while True:
        print("Enter group's name:")
        artist_name = input()
        try:
            print(get_link_on_artist(artist_name))
        except buisness_logic.core.exceptions.NotFoundArtistException:
            print("X3".center(30, '-'))
            print("Maybe, you think about:")
            print(f"\t{get_artist_info(artist_name, spotify=spotify)['artist_title']}")
            continue

        top = get_tracks_top(artist_name, spotify)
        print_top(top)

        print("*" * 80)


def print_top(top: list):
    for track in top:
        name = track['name']
        album_name = track['album_name']
        link_on_album = track['album_link']

        print(track['top_number'])

        print(
            f'\t{album_name} {track["release_date"]} {link_on_album}'
        )

        print(f'\t\t{name}')


if __name__ == "__main__":
    main()
