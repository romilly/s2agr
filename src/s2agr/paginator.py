from s2agr.urls import UrlBuilder


class Paginator:

    def __init__(self, requester, url_builder: UrlBuilder, limit=1000):
        self.requester = requester
        self.url_builder = url_builder
        self._limit = limit
        self._offset = 0

    def contents(self):
        while self.has_more_pages():
            for item in self.next_page_items():
                yield item

    def has_more_pages(self):
        return self._offset >= 0

    def next_page_items(self):
        self.url_builder = self.url_builder.for_range(self._offset, self._limit)
        results = self.requester.get(self.url_builder.get_url())
        self.update_offset_from(results)
        return self.data_from(results)

    @staticmethod
    def data_from(results):
        return (item for item in results['data'])

    def update_offset_from(self, results):
        self._offset = results['next'] if 'next' in results else -1
