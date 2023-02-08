import unittest

from s2ag.queries import q
from s2ag.urls import UrlBuilder


class UrlAndQueryTestCase(unittest.TestCase):
    def test_builds_url_for_query_with_fields(self):
        ub = UrlBuilder()
        query = q().with_keywords('covid', 'vaccination').with_fields('url', 'abstract', 'authors')
        actual_url = ub.for_search(query.parameters())
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=covid+vaccination&fields=url,abstract,authors'
        self.assertEqual(expected_url, actual_url)


if __name__ == '__main__':
    unittest.main()
