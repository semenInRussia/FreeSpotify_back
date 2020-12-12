from buisness_logic.dto import TrackDto
from buisness_logic.entities.track import Track

artist_name = "Metallica"
album_name = "Master of puppets"
track_name = "Master of puppets"


def test_init():
    Track(
        artist_name=artist_name,
        album_name=album_name,
        track_name=track_name
    )


def test_track_artist():
    track = Track(artist_name, album_name, track_name)

    assert track.artist.name == artist_name


def test_track_album():
    track = Track(artist_name, album_name, track_name)

    assert track.album.name == album_name


def test_track_create_from_dto():
    track_dto = TrackDto(
        artist_name=artist_name,
        album_name=album_name,
        name=track_name
    )

    track = Track.create_from_dto(track_dto)

    assert isinstance(track, Track)
    assert track.name == track_name
