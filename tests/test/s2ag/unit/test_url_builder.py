import unittest

from s2ag.queries import q
from s2ag.urls import UrlBuilder, UrlBuilderForSearch, UrlBuilderForSinglePaper


# TODO: add more examples
class UrlBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ub = UrlBuilder()

    def test_builds_url_for_search(self):
        actual_url = UrlBuilderForSearch().with_query(q().with_keywords('cerebellar','cortex')).get_url()
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=cerebellar+cortex'
        self.assertEqual(expected_url, actual_url)

    def test_builds_url_for_paper(self):
        actual_url = UrlBuilderForSinglePaper('649def34f8be52c8b66281af98ae884c09aef38b').get_url()
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/649def34f8be52c8b66281af98ae884c09aef38b'
        self.assertEqual(expected_url, actual_url)







