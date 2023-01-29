import unittest

import vcr

from s2ag.requester import WebRequester
from s2ag.researcher import Researcher
from test.s2ag.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)

class DatabaseCatalogueTestCase(DatabaseTest):
    @test_vcr.use_cassette
    def test_something(self):
        researcher = Researcher(WebRequester())
        self.check_total_row_count('paper', 0)
        paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = researcher.get_paper(paper_id)
        self.catalogue.write_paper(paper)
        self.check_total_row_count('paper', 1)


if __name__ == '__main__':
    unittest.main()
