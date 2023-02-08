from typing import Optional

from s2ag.queries import Query


class UrlBuilder:
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/'

    def __init__(self):
        self.query = Query()

    def with_query(self, query):
        self.query = self.query | query
        return self

    def for_search(self):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/search{query_part}'

    def get_query_string(self):
        items = self.query.parameters().items()
        return '' if len(items) == 0 else '?'+'&'.join(f'{key}={value}' for (key, value) in items)

    def for_paper(self, paper_id: str):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/{paper_id}{query_part}'

    def for_citations_of(self, paper_id: str):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/{paper_id}/citations{query_part}'



