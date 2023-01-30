import time
from abc import ABC, abstractmethod
from typing import Optional

import requests


class ThrottledRequesterException(Exception):
    pass


class Requester(ABC):

    @abstractmethod
    def get(self, url: str, parameters: Optional[str] = None) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, parameters, ids: dict) -> dict:
        pass


class ThrottledRequester(Requester):
    def __init__(self, delay=3.1):
        self.delay = delay
        self._last_request = time.monotonic()

    def get(self, url: str, parameters: Optional[str] = None) -> dict:
        self.throttle()
        if parameters is not None:
            url += '?' + parameters
        response = requests.get(url)
        if response.status_code != 200:
            raise ThrottledRequesterException(response.reason)
        return response.json()

    def throttle(self):
        gap = time.monotonic() - self._last_request
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last_request = time.monotonic()

    def post(self, url: str, parameters,  ids: dict) -> dict:
        self.throttle()
        if parameters is not None:
            url += '?' + parameters
        response = requests.post(url, json=ids)
        if response.status_code != 200:
            raise ThrottledRequesterException(response.reason)
        return response.json()
