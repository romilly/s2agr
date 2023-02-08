from abc import ABC, abstractmethod

from s2ag.queries import Query


class UrlBuilder(ABC):
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/'

    def __init__(self):
        self.query = Query()

    def with_query(self, query):
        self.query = self.query | query
        return self

    def get_query_string(self):
        items = self.query.parameters().items()
        return '' if len(items) == 0 else '?'+'&'.join(f'{key}={value}' for (key, value) in items)

    @abstractmethod
    def get_url(self):
        pass


class UrlBuilderForSearch(UrlBuilder):
    def get_url(self):
        return f'{self.BASE_URL}paper/search{self.get_query_string()}'


class UrlBuilderForSinglePaper(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url(self):
        return f'{self.BASE_URL}paper/{self.paper_id}{self.get_query_string()}'


class UrlBuilderForPaperCitations(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url(self):
        return f'{self.BASE_URL}paper/{self.paper_id}/citations{self.get_query_string()}'


class UrlBuilderForAuthor(UrlBuilder):
    def __init__(self, author_id: str):
        UrlBuilder.__init__(self)
        self.author_id = author_id

    def get_url(self):
        return f'{self.BASE_URL}author/{self.author_id}{self.get_query_string()}'
