from typing import Optional

from s2ag.queries import QueryBuilder


class UrlBuilder:
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/'

    def for_search(self, query: QueryBuilder):
        query_part = self.get_query_string(query.parameters())
        return f'{self.BASE_URL}paper/search{query_part}'

    @staticmethod
    def get_query_string(query: dict):
        if query is None or len(query) == 0:
            return ''
        return '?'+'&'.join(f'{key}={value}' for (key, value) in query.items())

    def for_paper(self, paper_id: str, query: Optional[dict] = None):
        query_part = self.get_query_string(query)
        return f'{self.BASE_URL}paper/{paper_id}{query_part}'


