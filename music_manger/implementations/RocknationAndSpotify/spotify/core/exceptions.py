class NotValidTokenException(Exception):
    """No Spotify token provided"""


class AccessTokenExpiredException(Exception):
    """The access Spotify token expired"""


class InvalidClientException(Exception):
    """Invalid Spotify client"""


class InvalidObjectIdException(Exception):
    """Invalid Spotify object(Artist, Album, Track)  id"""


class UndefinedErrorMessageException(Exception):
    """Undefined error in Spotify"""
