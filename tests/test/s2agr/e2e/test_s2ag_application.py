import unittest

import vcr
from hamcrest import assert_that, starts_with

from s2agr.builder import Builder
from test.s2agr.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGTestCase(DatabaseTest):
    def setUp(self) -> None:
        DatabaseTest.setUp(self)
        self.librarian = Builder().build()
        self.pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        self.aid = '6499892'

    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_paper(self):
        paper = self.librarian.get_paper(self.pid)
        self.assertEqual(paper.paper_id, self.pid)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")
        assert_that(paper.abstract, starts_with("We describe"))
        self.check_row_count('citation','cited_id',self.pid, 290)
        self.check_row_count('citation','citing_id',self.pid, 27)
        self.check_total_row_count('author',23)
        self.check_row_count('wrote','paper_id',self.pid, 23)

    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_author(self):
        author = self.librarian.get_author(self.aid)
        self.assertEqual(author.author_id, self.aid)
        self.check_row_count('author', 'author_id', self.aid, 1)

    @test_vcr.use_cassette
    def test_librarian_retrieves_known_author(self):
        author = self.librarian.get_author(self.aid)
        author = self.librarian.get_author(self.aid)
        self.assertEqual(author.author_id, self.aid)


if __name__ == '__main__':
    unittest.main()
