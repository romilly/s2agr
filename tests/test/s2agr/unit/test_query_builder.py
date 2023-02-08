import unittest
from hamcrest import assert_that, equal_to

from s2agr.urls import q


class QueryBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.query = q()

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

    def test_builds_query_with_offset_and_limit(self):
        q = self.query.in_range(100, 20)
        assert_that(q.parameters(), equal_to({'offset': '100', 'limit': '20'}))


    def test_builds_query_with_fields_and_keywords(self):
        q = self.query.with_keywords('covid', 'vaccination').with_fields('url', 'abstract', 'authors')
        assert_that(q.parameters(), equal_to({'query': 'covid+vaccination', 'fields': 'url,abstract,authors'}))
