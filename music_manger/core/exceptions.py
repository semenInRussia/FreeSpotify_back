class NotFoundAlbumException(Exception):
    message = "Album don't found."


class NotFoundArtistException(Exception):
    message = "Artist don't found."

class NotFoundTrackException(Exception):
    message = "Track don't found."
