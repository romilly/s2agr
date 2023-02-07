import unittest

from hamcrest import assert_that, contains_exactly, equal_to

import s2ag.queries


class QueryBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.q = s2ag.queries.q()

    def test_builds_simple_query(self):
        self.q.keywords('cerebellar', 'cortex')
        assert_that(self.q.parameters(), equal_to({'query': 'cerebellar+cortex'}))

    def test_builds_query_for_single_year(self):
        self.q.in_year(2020)
        assert_that(self.q.parameters(), equal_to({'year': '2020'}))

    def test_builds_query_for_year_range(self):
        self.q.between(2020, 2021)
        assert_that(self.q.parameters(), equal_to({'year': '2020-2021'}))

    def test_builds_query_before_year(self):
        self.q.before(2021)
        assert_that(self.q.parameters(), equal_to({'year': '-2021'}))

    def test_builds_query_after_year(self):
        self.q.after(2020)
        assert_that(self.q.parameters(), equal_to({'year': '2020-'}))