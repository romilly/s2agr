import unittest

from s2agr.urls import UrlBuilderForSearch, q


class UrlAndQueryTestCase(unittest.TestCase):
    def test_builds_url_for_query_with_fields(self):
        query = q().with_keywords('covid', 'vaccination').with_fields('url', 'abstract', 'authors')
        actual_url = UrlBuilderForSearch().with_query(query).get_url()
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=covid+vaccination&fields=url,abstract,authors'
        self.assertEqual(expected_url, actual_url)


if __name__ == '__main__':
    unittest.main()
