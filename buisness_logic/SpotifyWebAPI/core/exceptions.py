class NotValidTokenException(Exception):
    message = 'No token provided'

class AccessTokenExpiredException(Exception):
    message = 'The access token expired'

class UndefinedErrorMessageException(Exception):
    message = 'Undefined error'

class InvalidClientException(Exception):
    message = 'Invalid client'

class UndefinedArtistException(Exception):
    message = 'You are enter undefined artist'

class NotResultSearchException(Exception):
    message = 'Not result search'


