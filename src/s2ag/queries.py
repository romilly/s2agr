
class QueryBuilder:
    def __init__(self):
        self._parameters = {}

    def keywords(self, *keywords: str) -> 'QueryBuilder':
        self._parameters['query'] = '+'.join(keywords)
        return self

    def parameters(self):
        return self._parameters

    def in_year(self, year: int) -> 'QueryBuilder':
        self._parameters['year']  = str(year)
        return self

    def between(self, start_year: int, end_year: int)-> 'QueryBuilder':
        self._parameters['year']  = f'{start_year}-{end_year}'
        return self

    def before(self, end_year: int) -> 'QueryBuilder':
        self._parameters['year']  = f'-{end_year}'
        return self

    def after(self, start_year) -> 'QueryBuilder':
        self._parameters['year']  = f'{start_year}-'
        return self


def q() -> QueryBuilder:
    return QueryBuilder()
