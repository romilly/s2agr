from typing import Any, Optional


class Paginator:

    def __init__(
                self,
                requester,
                url: str,
                fields,
                url_generator: Optional[callable] = None,
                limit = 1000,
            ) -> None:

        self.requester = requester
        self._url = url
        self._fields = fields
        self.url_generator = url_generator
        self._limit = limit
        self._offset = 0

    def contents(self) -> Any:
        while True:
            items = self.get_next_page()
            for item in items:
                yield item
            if self._offset < 0:
                break

    def get_next_page(self) -> list:
        results = self.requester.get(
                self._url,
                self.parameters(),
            )

        self._offset = results['next'] if 'next' in results else -1
        return [item for item in results['data']]

    def parameters(self) -> str:

        fields = ','.join(self._fields)
        result = f'&fields={fields}'

        result += f'&offset={self._offset}'
        result += f'&limit={self._limit}'
        return result

    def new_contents(self):
        while True:
            items = self.get_next_page()
            for item in items:
                yield item
            if self._offset < 0:
                break
