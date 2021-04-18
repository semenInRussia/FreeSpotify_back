import base64

from loguru import logger

import my_request
from settings import spotify
from .core.exceptions import AccessTokenExpiredException
from .core.exceptions import InvalidClientException
from .core.exceptions import InvalidObjectIdException
from .core.exceptions import NotValidTokenException
from .core.exceptions import UndefinedErrorMessageException

version_api = 'v1'
base_url = f"https://api.spotify.com/{version_api}/"


def _check_json_spotify_response(json_response: dict):
    if not _is_response_has_error(json_response):
        return

    all_excepted_exceptions = [
        NotValidTokenException,
        AccessTokenExpiredException,
        InvalidObjectIdException,
        InvalidClientException
    ]

    current_exception_message = json_response["error"]["message"]

    for exception in all_excepted_exceptions:
        if exception.message == current_exception_message:
            raise exception

    logger.warning(current_exception_message)

    raise UndefinedErrorMessageException


def _is_response_has_error(json_response: dict):
    return json_response.get('error')


class SpotifyAuthenticator:
    @property
    def token(self) -> str:
        self._set_new_token()

        return self._token

    def _set_new_token(self):
        self._token = self._create_token()

    def _create_token(self) -> str:
        url = "https://accounts.spotify.com/api/token"

        # Encode as Base64
        message = f"{spotify.SPOTIFY_CLIENT_ID}:{spotify.SPOTIFY_CLIENT_SECRET}"
        base64_message = self._encode_as_base64(message)

        headers = {
            'Authorization': f"Basic {base64_message}"
        }
        data = {
            'grant_type': "client_credentials"
        }

        auth_json_data = my_request.get_json(
            url,
            method_name='post',
            headers=headers,
            data=data
        )

        _check_json_spotify_response(auth_json_data)

        token = auth_json_data['access_token']

        return token

    @staticmethod
    def _encode_as_base64(message: str) -> str:
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')

        return base64_message


class SpotifyJsonParser:
    def __init__(self):
        self._authenticator = SpotifyAuthenticator()

    def get_json_from_spotify(
            self,
            second_part_of_links: str,
            method_name: str = 'get',
            data: dict = None,
            **params
    ) -> dict:
        url = base_url + second_part_of_links

        headers = {
            "Authorization": "Bearer " + self._authenticator.token
        }

        response_data = my_request.get_json(
            url,
            method_name=method_name,

            params=params,
            headers=headers,
            data=data
        )

        _check_json_spotify_response(response_data)

        return response_data


class SpotifyCore:
    """
    Object for work with base operations with spotify on level with rest api.

    For additional info watch https://api.spotify.com/v1/search.
    """

    def __init__(self):
        self._json_parser = SpotifyJsonParser()

    def search(self, q: str, type_: str, market: str = None, limit: int = 1, offset: int = 0) -> dict:
        """
        Search ANY in Spotify.

        Info from https://developer.spotify.com/documentation/web-api/reference/#endpoint-search .

        :param q: str
        Search query keywords and optional field filters and operators.
        For example:
        q="AC DC - Down Payment Blue".
        :param type_: str
        A comma-separated list of item types to search across.

        Valid types are:
        * album
        * artist
        * playlist
        * track
        * show
        * episode.

        Search results include hits from all the specified item types.

        :param market: str | None
        An ISO 3166-1 alpha-2 country code or the string from_token.
        If a country code is specified, only content that is playable in that market is returned.
        Note:
        - Playlist results are not affected by the market parameter.
        - If market is set to from_token, and a valid access token is specified in the request header, only content
          playable in the country associated with the user account, is returned.
        - Users can view the country that is associated with their account in the account settings. A user must grant
          access to the user-read-private scope prior to when the access token is issued. 	String 	Optional

        :param limit: int | None
        Maximum number of results to return.
        * Default: 20
        * Minimum: 1
        * Maximum: 50
        Note: The limit is applied within each type, not on the total response.
        For example, if the limit value is 3 and the type is artist,album, the response contains 3 artists and 3 albums. 	Integer 	Optional

        :param offset: int
        The index of the first result to return.
        * Default: 0 (the first result).
        * Maximum offset (including limit): 1,000.
        Use with limit to get the next page of search results.
       """

        return self._json_parser.get_json_from_spotify(
            second_part_of_links='search',

            q=q,
            type=type_,
            limit=limit,
            offset=offset,
            market=market
        )

    def get_top_tracks(self, artist_id: str, market: str = 'US') -> dict:
        """
        Get Artist's top.

        Info from https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-an-artists-top-tracks .

        :param artist_id: str
        The Spotify ID for the artist 	String 	Required
        Query Parameter 	Type 	Required
        :param market: str | None
        An ISO 3166-1 alpha-2 country code or the string from_token. Synonym for country.
        """

        url = f'artists/{artist_id}/top-tracks'

        return self._json_parser.get_json_from_spotify(
            second_part_of_links=url,

            country=market
        )

    def get_album_info(self, album_ids: str, market: str = 'ES'):
        """
        Get info about current albums by ids.
        Info from https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-multiple-albums

        :param album_ids: str
        A comma-separated list of the Spotify IDs for the albums. Maximum: 20 IDs.
        :param market: str | None
        An ISO 3166-1 alpha-2 country code or the string from_token. Provide this parameter if you want to apply Track
        Relinking.
        """

        return self._json_parser.get_json_from_spotify(
            second_part_of_links='albums',

            market=market,
            ids=album_ids
        )

    def get_tracks_of_album(self, album_id: str):
        url = f'albums/{album_id}/tracks'

        return self._json_parser.get_json_from_spotify(url)
