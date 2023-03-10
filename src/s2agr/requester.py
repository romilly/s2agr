import time
from abc import ABC, abstractmethod
from typing import Optional

import requests

REQUEST_OK = 200
BAD_REQUEST = 400


class ThrottledRequesterException(Exception):
    pass


class Requester(ABC):

    @abstractmethod
    def get(self, url: str) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, ids: dict) -> dict:
        pass


class ThrottledRequester(Requester):
    STANDARD_THROTTLING_DELAY = 3.1

    def __init__(self, delay=STANDARD_THROTTLING_DELAY):
        self.delay = delay
        self._last_request = time.monotonic()

    def get(self, url: str) -> dict:
        self.throttle()
        response = requests.get(url)
        if response.status_code == BAD_REQUEST:
            raise ThrottledRequesterException(response.json()['error'])
        if response.status_code != REQUEST_OK:
            raise ThrottledRequesterException(response.reason)
        result = response.json()
        return result

    def throttle(self):
        gap = time.monotonic() - self._last_request
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self._last_request = time.monotonic()

    def post(self, url: str,  ids: dict) -> dict:
        self.throttle()
        response = requests.post(url, json=ids)
        if response.status_code != REQUEST_OK:
            raise ThrottledRequesterException(response.reason)
        return response.json()
