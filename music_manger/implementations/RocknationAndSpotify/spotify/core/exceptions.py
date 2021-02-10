class NotValidTokenException(Exception):
    """No Spotify token provided"""
    message = 'No token provided'


class AccessTokenExpiredException(Exception):
    """The access Spotify token expired"""
    message = 'The access token expired'


class InvalidClientException(Exception):
    """Invalid Spotify client"""
    message = 'Invalid client'


class InvalidObjectIdException(Exception):
    """Invalid Spotify object(Artist, Album, Track)  id"""
    message = 'invalid id'


class UndefinedErrorMessageException(Exception):
    """Undefined error in Spotify"""
