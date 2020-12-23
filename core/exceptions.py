class NotFoundAlbumException(Exception):
    message = "Album don't find."


class NotFoundArtistException(Exception):
    message = "Artist don't find."


class NotValidMethodNameExceptions(Exception):
    txt = 'You are write not valid method name'

class NotFoundCommandException(Exception):
    txt = 'Your Alias Is Not Defined.'
