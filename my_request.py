import json

import requests
from bs4 import BeautifulSoup

from core.exceptions import NotValidMethodNameExceptions


class Requester:
    methods = {
        'get': requests.get,
        'post': requests.post,
    }

    def get_bs(self, url: str):
        html = self.get_content(url)

        return BeautifulSoup(html, "html.parser")

    def get_json(self, url: str, method_name: str = 'get'):
        return json.loads(self.get_content(url, method_name))

    def get_content(self, url: str, method_name: str = 'get'):

        return self.create_request(url, method_name).text

    def create_request(self, url: str, method_name: str = 'get'):
        method = self._get_method(method_name)

        return method(url)

    def _get_method(self, method_name: str):
        try:
            return self.methods[method_name]
        except AttributeError:
            raise NotValidMethodNameExceptions
