import json
import unittest

from hamcrest import assert_that, equal_to, contains_exactly

from s2ag.paper import Paper


def read(filename):
    with open(filename) as f:
        return f.read()


class PaperCitationsTestCase(unittest.TestCase):
    def test_paper_knows_citating_ids(self):
        jd = json.loads(read('test/s2ag/data/samples/sample_02.json'))
        paper = Paper(jd)
        citing_ids = paper.citing_ids()
        assert_that(citing_ids, contains_exactly(
            '9088b5478fc706f368d2d1fd5661aba9384d782b',
            '1dd4b9b27250e20172260db7fbb4392ff5fec872',
            '1ff4ab59f46afb6ad6c79f9c25852e5da09a1125'
        ))


if __name__ == '__main__':
    unittest.main()
