import base64

import requests
from loguru import logger

from settings import spotify

from .core.exceptions import UndefinedErrorMessageException
from .core.exceptions import InvalidObjectIdException
from .core.exceptions import AccessTokenExpiredException
from .core.exceptions import NotValidTokenException
from .core.exceptions import InvalidClientException

version_api = 'v1'
base_url = f"https://api.spotify.com/{version_api}/"


class ExceptionsMangerSpotifyCore:
    @staticmethod
    def _raise_spotify_web_api_errors(response_data: dict):
        if not response_data.get('error'):
            return None

        exceptions = [
            NotValidTokenException,
            AccessTokenExpiredException,
            InvalidObjectIdException,
        ]

        current_error_message = response_data["error"]["message"]

        for exception in exceptions:
            if exception.message == current_error_message:
                raise exception
        else:
            logger.warning(current_error_message)

            raise UndefinedErrorMessageException


class AuthenticationSpotifyMixIn:
    def __init__(self):
        # Set token
        self._set_new_token()

    @property
    def token(self) -> str:
        self._set_new_token()

        return self._token

    @staticmethod
    def _encode_as_base64(message: str) -> str:
        messageBytes = message.encode('ascii')
        base64Bytes = base64.b64encode(messageBytes)
        base64Message = base64Bytes.decode('ascii')

        return base64Message

    def _set_new_token(self):
        self._token = self._create_token()

    def _create_token(self) -> str:
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        # Encode as Base64
        message = f"{spotify.SPOTIFY_CLIENT_ID}:{spotify.SPOTIFY_CLIENT_SECRET}"
        base64Message = self._encode_as_base64(message)

        headers['Authorization'] = f"Basic {base64Message}"
        data['grant_type'] = "client_credentials"

        auth_json_data = self._post_response_JSON(url, headers=headers, data=data)

        try:
            token = auth_json_data['access_token']
        except KeyError:
            if auth_json_data['error_description'] == InvalidClientException:
                raise InvalidClientException
            else:
                raise UndefinedErrorMessageException
        else:
            return token


class SendResponse(AuthenticationSpotifyMixIn, ExceptionsMangerSpotifyCore):
    @staticmethod
    def _get_response(url: str, params: dict = None, headers: dict = None, data: dict = None) -> requests.Response:
        return requests.get(url, params=params, headers=headers, data=data)

    def _get_response_JSON(self, url: str, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        return self._get_response(url, params=params, headers=headers, data=data).json()

    def _get_response_JSON_with_link_spotify(self, second_part_of_links: str, data: dict = None, **params) -> dict:
        url = base_url + second_part_of_links

        headers = {
            "Authorization": "Bearer " + self.token
        }

        response_data = self._get_response_JSON(url, params=params, headers=headers, data=data)
        self._raise_spotify_web_api_errors(response_data)

        return response_data

    @staticmethod
    def _post_response(url: str, params: dict = None, headers: dict = None, data: dict = None) -> requests.Response:
        return requests.post(url, params=params, headers=headers, data=data)

    def _post_response_JSON(self, url: str, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        return self._post_response(url, params=params, headers=headers, data=data).json()

    def _post_response_JSON_with_link_spotify(self, second_part_of_links: str, params: dict = None,
                                              data: dict = None) -> dict:
        self._set_new_token()

        url = base_url + second_part_of_links

        headers = {
            "Authorization": "Bearer " + self.token
        }

        return self._post_response_JSON(url, params=params, headers=headers, data=data)


class SpotifyCore(SendResponse):
    """
    Object for work for base operation with spotify.
    For example, search( q: str, type_: str, marker: str = None, limit: int = 1, offset: int = 0) -> dict,
    return response from https://api.spotify.com/v1/search.
    """

    def search(self, q: str, type_: str, marker: str = None, limit: int = 1, offset: int = 0) -> dict:
        """Search tracks or artist on Spotify"""
        params = {
            'q': q,
            'type': type_,
            'limit': limit,
            'offset': offset,
        }

        if marker:
            params['marker'] = marker
        return self._get_response_JSON_with_link_spotify(second_part_of_links='search',
                                                         **params)

    def get_top_tracks(self, artist_id: str, country: str = 'US') -> dict:
        return self._get_response_JSON_with_link_spotify(second_part_of_links=f'artists/{artist_id}/top-tracks',
                                                         country=country)

    def get_album_info(self, album_ids: str, market: str = 'ES'):
        logger.info(f"album_ids = {album_ids}")

        return self._get_response_JSON_with_link_spotify(second_part_of_links=f'albums',
                                                         market=market,
                                                         ids=album_ids)

    def get_tracks_of_album(self, album_id: str):
        return self._get_response_JSON_with_link_spotify(f'albums/{album_id}/tracks')
