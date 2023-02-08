from typing import Optional


class QueryBuilder:
    def __init__(self, parameters: Optional[dict] = None):
        self._parameters = {} if parameters is None else parameters

    def __or__(self, other: 'QueryBuilder'):
        d = dict(self.parameters(), **other.parameters())
        return QueryBuilder(d)

    def with_keywords(self, *keywords: str) -> 'QueryBuilder':
        self._parameters['query'] = '+'.join(keywords)
        return self.copy()

    def in_year(self, year: int) -> 'QueryBuilder':
        self._parameters['year']  = str(year)
        return self.copy()

    def between(self, start_year: int, end_year: int)-> 'QueryBuilder':
        self._parameters['year']  = f'{start_year}-{end_year}'
        return self.copy()

    def before(self, end_year: int) -> 'QueryBuilder':
        self._parameters['year']  = f'-{end_year}'
        return self.copy()

    def after(self, start_year) -> 'QueryBuilder':
        self._parameters['year']  = f'{start_year}-'
        return self.copy()

    def with_fields(self, *fields: str) -> 'QueryBuilder':
        self._parameters['fields'] = ','.join(fields)
        return self.copy()

    def in_range(self, offset: int, limit: int):
        self._parameters['offset'] = str(offset)
        self._parameters['limit'] = str(limit)
        return self.copy()

    def parameters(self) -> dict:
        return self._parameters

    def copy(self) -> 'QueryBuilder':
        return QueryBuilder(self.parameters().copy())



def q() -> QueryBuilder:
    return QueryBuilder()
