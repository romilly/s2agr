import unittest

import vcr

from s2agr.builder import Builder
from test.s2agr.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGCachingTestCase(DatabaseTest):

    @test_vcr.use_cassette
    def test_librarian_retrieves_known_paper_from_database(self):
        librarian = Builder().build()
        fly_paper_id = 'e2e1aa8b8b1dfed9c65589d5293acbae4cbe061a' # small set of citations
        self.check_total_row_count('paper', 0)
        librarian.get_paper(fly_paper_id)
        self.check_total_row_count('paper', 1)
        s2ag_paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        librarian.get_paper(s2ag_paper_id)
        self.check_total_row_count('paper', 2)
        librarian.get_paper(fly_paper_id)
        self.check_total_row_count('paper', 2)


if __name__ == '__main__':
    unittest.main()
