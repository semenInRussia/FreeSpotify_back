import json

import requests
from bs4 import BeautifulSoup


class Requester:
    def get_bs(self, url: str):
        html = self.get_content(url)

        return BeautifulSoup(html, "html.parser")

    def get_json(self, url: str, method_name: str = 'get'):
        return json.loads(self.get_content(url, method_name))

    def get_content(self, url: str, method_name: str = 'get'):
        return self.create_request(url, method_name).text

    @staticmethod
    def create_request(url: str, method_name: str = 'get'):
        return requests.request(method_name, url)
