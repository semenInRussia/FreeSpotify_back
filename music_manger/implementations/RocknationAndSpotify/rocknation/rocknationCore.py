import requests
from bs4 import BeautifulSoup

from .core.exceptions import NotValidMethodNameExceptions


class RocknationCore:
    methods = {
        'get': requests.get,
        'post': requests.post,
    }

    def get_bs(self, url: str):
        html = self.get_html(url)

        return BeautifulSoup(html, "html.parser")

    def get_html(self, url: str, method_name: str = 'get'):

        method = self._get_method(method_name)

        return method(url).text

    def _get_method(self, method_name: str):
        try:
            return self.methods[method_name]
        except AttributeError:
            raise NotValidMethodNameExceptions
