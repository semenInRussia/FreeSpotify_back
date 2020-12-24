from entities import Artist, Track


def print_top_item(index, track: Track):
    num_in_top = index + 1

    print(f"\t{num_in_top}. {track.name}")
    print(f"\t\t{track.album.name} ({track.album.release_date})")
    print(f"\t URL - {track.album.link}")
    print()


def print_artist_info(artist: Artist):
    print(artist.name)
    print(f"\tURL - {artist.link}")
    print()


def print_artist_top(artist_name: str):
    artist = Artist(artist_name)
    top = artist.top

    print_artist_info(artist)

    for i, track in enumerate(top):
        print_top_item(i, track)


def print_and_ask_artist_top():
    artist_name = input('Enter artist name:')

    print_artist_top(artist_name)


def print_artist_tops():
    while True:
        print_and_ask_artist_top()


def by():
    print()
    print('Good Luck!')
    print()


def run():
    try:
        print_artist_tops()
    except KeyboardInterrupt:
        by()


if __name__ == '__main__':
    run()
