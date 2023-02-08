from typing import Any, Optional

from s2agr.urls import UrlBuilder


class Paginator:

    def __init__(self, requester,
                 url_builder: UrlBuilder,
                 limit=1000):
        self.requester = requester
        self.url_builder = url_builder
        self._limit = limit
        self._offset = 0

    def contents(self):
        while True:
            items = self.next_page()
            for item in items:
                yield item
            if self._offset < 0:
                break

    def next_page(self):
        self.url_builder = self.url_builder.in_range(self._offset, self._limit)
        results = self.requester.get(
            self.url_builder.get_url(),
        )
        self._offset = results['next'] if 'next' in results else -1
        return [item for item in results['data']]
