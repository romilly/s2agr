from typing import Optional
from abc import ABC, abstractmethod


class UrlBuilder(ABC):
    """
    abstract base class for the builders used to create S2AG RESTful Urls.

    S2AG is the Semantic Scholar Academic Graph.

    See https://api.semanticscholar.org/api-docs/graph for API documentation.

    Semantic Scholar is a free, AI-powered research tool for scientific literature,
    based at the Allen Institute for AI.
    For more information, see https://www.semanticscholar.org/product/api

    """
    BASE_URL = 'https://api.semanticscholar.org/graph/v1/'

    def __init__(self):
        self.query = Query()

    def with_query(self, another_query) -> 'UrlBuilder':
        """
        combines current query with another query
        """
        self.query = self.query & another_query
        return self

    def get_query_string(self) -> str:
        """
        returns the full RESTful url needed to retrieve a resource from S2AG
        """
        return self.query.query_string()

    def get_url(self) -> str:
        return self.get_url_stem()+self.get_query_string()

    @abstractmethod
    def get_url_stem(self) -> str:
        """
        returns the scheme, authority and path portion of the final url
        """
        pass

    def for_range(self, offset, limit):
        return self.with_query(q().in_range(offset, limit))

    def with_keywords(self, *keywords):
        return self.with_query(q().with_keywords(*keywords))


class UrlBuilderForSearch(UrlBuilder):
    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}paper/search'


class UrlBuilderForSinglePaper(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}paper/{self.paper_id}'


class UrlBuilderForPapers(UrlBuilder):

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}paper/batch'


class UrlBuilderForPaperCitations(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}paper/{self.paper_id}/citations'


class UrlBuilderForPaperReferences(UrlBuilder):
    def __init__(self, paper_id: str):
        UrlBuilder.__init__(self)
        self.paper_id = paper_id

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}paper/{self.paper_id}/references'


class UrlBuilderForAuthor(UrlBuilder):
    def __init__(self, author_id: str):
        UrlBuilder.__init__(self)
        self.author_id = author_id

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}author/{self.author_id}'


class UrlBuilderForPapersByAuthor(UrlBuilder):
    def __init__(self, author_id: str):
        UrlBuilder.__init__(self)
        self.author_id = author_id

    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}author/{self.author_id}/papers'


class UrlBuilderForAuthors(UrlBuilder):
    def get_url_stem(self) -> str:
        return f'{self.BASE_URL}author/batch'


class Query:
    """
    A query object for use with UrlBuilders.

     A UrlBuilder creates a URL to retrieve data from the Semantic Scholar Academic Graph.
     A Query object is used to generate the query portion of the generated URL.

    Query implements a fluent interface as described in https://martinfowler.com/bliki/FluentInterface.html
    Query objects are immutable.
    """

    def __init__(self, query_parameters: Optional[dict] = None):
        self._query_parameters = {} if query_parameters is None else query_parameters

    def __and__(self, other: 'Query'):
        """
        Create a new Query that combines this with the constraints in another query.

        If the two queries have conflicting constraints the second query takes precedence.
        TODO: verify in a Unit Test!

        Usage: q1 = q2 & q3
        """
        d = dict(self.parameters(), **other.parameters())
        return Query(d)

    def with_keywords(self, *keywords: str) -> 'Query':
        """
        Sets the keywords to be used in the URL.

        Multiple keywords are separated by `+`.
        """
        self._query_parameters['query'] = '+'.join(keywords)
        return self.copy()

    def in_year(self, year: int) -> 'Query':
        """

        """
        self._query_parameters['year'] = str(year)
        return self.copy()

    def between(self, start_year: int, end_year: int) -> 'Query':
        self._query_parameters['year'] = f'{start_year}-{end_year}'
        return self.copy()

    def before(self, end_year: int) -> 'Query':
        self._query_parameters['year'] = f'-{end_year}'
        return self.copy()

    def after(self, start_year) -> 'Query':
        self._query_parameters['year'] = f'{start_year}-'
        return self.copy()

    def with_fields(self, *fields: str) -> 'Query':
        self._query_parameters['fields'] = ','.join(fields)
        return self.copy()

    def in_range(self, offset: int, limit: int):
        self._query_parameters['offset'] = str(offset)
        self._query_parameters['limit'] = str(limit)
        return self.copy()

    def query_string(self):
        items = self.parameters().items()
        if len(items) == 0:
            result = ''
        else:
            result = '?' + '&'.join(f'{key}={value}' for (key, value) in items)
        return result

    def parameters(self) -> dict:
        return self._query_parameters

    def copy(self) -> 'Query':
        """
        Create a copy to enable safe reuse of shared partial queries.

        See http://www.natpryce.com/articles/000724.html for an explanation of the issue and solution.
        """
        return Query(self.parameters().copy())


def q() -> Query:
    return Query()

