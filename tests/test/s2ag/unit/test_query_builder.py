import unittest

from hamcrest import assert_that, contains_exactly, equal_to


class QueryBuilder:
    def __init__(self):
        self._keywords = []

    def keywords(self, *keywords: str):
        self._keywords = keywords
        return self

    def parameters(self):
        return {'query': '+'.join(self._keywords)}


def q():
    return QueryBuilder()


class QueryBuilderTestCase(unittest.TestCase):
    def test_builds_simple_query(self):
        qb = q().keywords('cerebellar','cortex')
        assert_that(qb.parameters(), equal_to({'query': 'cerebellar+cortex'}))

