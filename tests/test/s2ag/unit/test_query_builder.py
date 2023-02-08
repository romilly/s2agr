import unittest
from hamcrest import assert_that, equal_to

import s2ag.queries


class QueryBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.query = s2ag.queries.q()

    def test_builds_simple_query(self):
        q = self.query.with_keywords('cerebellar', 'cortex')
        assert_that(q.parameters(), equal_to({'query': 'cerebellar+cortex'}))

    def test_builds_query_for_single_year(self):
        q = self.query.in_year(2020)
        assert_that(q.parameters(), equal_to({'year': '2020'}))

    def test_builds_query_for_year_range(self):
        q = self.query.between(2020, 2021)
        assert_that(q.parameters(), equal_to({'year': '2020-2021'}))

    def test_builds_query_before_year(self):
        q = self.query.before(2021)
        assert_that(q.parameters(), equal_to({'year': '-2021'}))

    def test_builds_query_after_year(self):
        q = self.query.after(2020)
        assert_that(q.parameters(), equal_to({'year': '2020-'}))

    def test_builds_query_with_fields(self):
        q = self.query.with_keywords('covid', 'vaccination').with_fields('url', 'abstract', 'authors')
        assert_that(q.parameters(), equal_to({'query': 'covid+vaccination', 'fields': 'url,abstract,authors'}))
