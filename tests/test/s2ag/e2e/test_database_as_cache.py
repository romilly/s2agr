import unittest

import vcr

from s2ag.librarian import Librarian, Researcher
from s2ag.persistence.database_catalogue import DatabaseCatalogue, test_connection
from s2ag.requester import WebRequester
from test.s2ag.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGCachingTestCase(DatabaseTest):

    @test_vcr.use_cassette
    def test_librarian_retrieves_known_paper_from_database(self):
        requester = WebRequester()
        catalogue = DatabaseCatalogue(test_connection())
        librarian = Librarian(Researcher(requester), catalogue)
        fly_paper_id = '6da2905bef6b50736660028ce5d11db3206095c1'
        self.check_total_row_count('paper', 0)
        paper = librarian.get_paper(fly_paper_id)
        self.check_total_row_count('paper', 1)
        s2ag_paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = librarian.get_paper(s2ag_paper_id)
        self.check_total_row_count('paper', 2)
        paper = librarian.get_paper(fly_paper_id)
        self.check_total_row_count('paper', 2)


if __name__ == '__main__':
    unittest.main()
