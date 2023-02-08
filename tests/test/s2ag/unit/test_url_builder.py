import unittest

from s2ag.urls import UrlBuilder


# TODO: add more examples
class UrlBuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ub = UrlBuilder()

    def test_builds_url_for_search(self):
        url = self.ub.for_search({'query': 'cerebellar+cortex'})
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=cerebellar+cortex'
        self.assertEqual(expected_url, url)



    def test_builds_url_for_paper(self):
        actual_url = self.ub.for_paper('649def34f8be52c8b66281af98ae884c09aef38b')
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/649def34f8be52c8b66281af98ae884c09aef38b'
        self.assertEqual(expected_url, actual_url)





