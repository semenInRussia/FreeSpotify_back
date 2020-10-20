import base64

import requests
from loguru import logger

from buisness_logic.SpotifyWebAPI.core.exceptions import InvalidClientException, UndefinedErrorMessageException, \
    NotValidTokenException, AccessTokenExpiredException, InvalidClientIdException

version_api = 'v1'
base_url = f"https://api.spotify.com/{version_api}/"

spotify_client_id = "1878579b79fd4d30b106622791eaa706"
spotify_client_secret = "09ece004e71740da8f003ba333c7f887"


class Spotify:
    """
    Object for work with spotify.
    """

    def __init__(self):
        # Set token
        self._set_new_token()

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
                                                         params=params)

    @property
    def token(self) -> str:
        return self._token

    def get_top_tracks(self, artist_id: str, country: str = 'US') -> dict:
        return self._get_response_JSON_with_link_spotify(second_part_of_links=f'artists/{artist_id}/top-tracks',
                                                         params={
                                                             "country": country
                                                         })

    def _create_token(self) -> str:
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}

        # Encode as Base64
        message = f"{spotify_client_id}:{spotify_client_secret}"
        base64Message = self._encode_as_base64(message)

        headers['Authorization'] = f"Basic {base64Message}"
        data['grant_type'] = "client_credentials"

        auth_json_data = self._post_response_JSON(url, headers=headers, data=data)

        logger.debug(auth_json_data)

        try:
            token = auth_json_data['access_token']
        except KeyError:
            if auth_json_data['error_description'] == InvalidClientException:
                raise InvalidClientException
            else:
                raise UndefinedErrorMessageException
        else:
            return token

    def _set_new_token(self):
        self._token = self._create_token()

    @staticmethod
    def _get_response(url: str, params: dict = None, headers: dict = None, data: dict = None) -> requests.Response:
        return requests.get(url, params=params, headers=headers, data=data)

    def _get_response_JSON(self, url: str, params: dict = None, headers: dict = None, data: dict = None) -> dict:
        return self._get_response(url, params=params, headers=headers, data=data).json()

    def _get_response_JSON_with_link_spotify(self, second_part_of_links: str, params: dict = None,
                                             data: dict = None) -> dict:
        url = base_url + second_part_of_links

        headers = {
            "Authorization": "Bearer " + self.token
        }

        response_data = self._get_response_JSON(url, params=params, headers=headers, data=data)
        self._raise_spotify_web_api_errors(response_data)

        return response_data

    @staticmethod
    def _raise_spotify_web_api_errors(response_data: dict):
        # Here not errors
        if not response_data.get('error'):
            return None

        logger.warning(response_data['error']['message'])
        # Here are errors
        if response_data['error']['message'] == NotValidTokenException.message:
            raise NotValidTokenException
        elif response_data['error']['message'] == AccessTokenExpiredException.message:
            raise AccessTokenExpiredException
        elif response_data['error']['message'] == InvalidClientIdException.message:
            raise InvalidClientIdException
        else:
            raise UndefinedErrorMessageException

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

    @staticmethod
    def _encode_as_base64(message: str) -> str:
        messageBytes = message.encode('ascii')
        base64Bytes = base64.b64encode(messageBytes)
        base64Message = base64Bytes.decode('ascii')

        return base64Message
