from abc import ABC, abstractmethod
from typing import Optional

import requests


class Requester(ABC):

    @abstractmethod
    def get(self, url: str, parameters: Optional[str] = None) -> dict:
        pass


class WebRequester(Requester):

    def get(self, url: str, parameters: Optional[str] = None):
        if parameters is not None:
            url += '?' + parameters
        response = requests.get(url)
        return response.json()

