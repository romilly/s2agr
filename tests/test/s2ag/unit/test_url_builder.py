import unittest


class UrlBuilder:
    def for_query(self, query: dict):
        query_part = '&'.join(f'{key}={value}' for (key, value) in query.items())
        return f'https://api.semanticscholar.org/graph/v1/paper/search?{query_part}'


class UrlBuilderTestCase(unittest.TestCase):
    def test_builds_url_for_query(self):
        ub = UrlBuilder()
        url = ub.for_query({'query': 'cerebellar+cortex'})
        expected_url = 'https://api.semanticscholar.org/graph/v1/paper/search?query=cerebellar+cortex'
        self.assertEqual(expected_url, url)


if __name__ == '__main__':
    unittest.main()
