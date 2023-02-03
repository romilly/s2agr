import unittest

import vcr
from hamcrest import assert_that, starts_with

from s2ag.builder import Builder
from s2ag.librarian import Librarian, Researcher
from s2ag.monitor import PrintingMonitor
from s2ag.persistence.database_catalogue import DatabaseCatalogue, test_connection
from s2ag.requester import ThrottledRequester
from test.s2ag.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGTestCase(DatabaseTest):
    def setUp(self) -> None:
        DatabaseTest.setUp(self)
        self.librarian = Builder().with_monitor(PrintingMonitor()).build()
        self.pid = '649def34f8be52c8b66281af98ae884c09aef38b'


    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_paper(self):
        paper = self.librarian.get_paper(self.pid)
        self.assertEqual(paper.paper_id, self.pid)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")
        assert_that(paper.abstract, starts_with("We describe"))
        self.check_row_count('citation','cited_id',self.pid, 288)







if __name__ == '__main__':
    unittest.main()
