from typing import Optional

from s2ag.queries import Query


class UrlBuilder:
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/'

    def __init__(self):
        self.query = Query()

    def with_query(self, query):
        self.query = self.query | query
        return self

    def get_query_string(self):
        items = self.query.parameters().items()
        return '' if len(items) == 0 else '?'+'&'.join(f'{key}={value}' for (key, value) in items)

    # def for_citations_of(self, paper_id: str):
    #     query_part = self.get_query_string()
    #     return f'{self.BASE_URL}paper/{paper_id}/citations{query_part}'

# TODO: replace method calls by sub-classes


class UrlBuilderForSearch(UrlBuilder):
    def get_url(self):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/search{query_part}'


class UrlBuilderForSinglePaper(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url(self):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/{self.paper_id}{query_part}'


class UrlBuilderForPaperCitations(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url(self):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}paper/{self.paper_id}/citations{query_part}'

class UrlBuilderForAuthor(UrlBuilder):
    def __init__(self, author_id: str):
        UrlBuilder.__init__(self)
        self.author_id = author_id

    def get_url(self):
        query_part = self.get_query_string()
        return f'{self.BASE_URL}author/{self.author_id}{query_part}'








