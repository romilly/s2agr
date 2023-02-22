import unittest

import vcr
from hamcrest import assert_that, starts_with

from s2agr.builder import Builder
from test.s2agr.helpers.database_test import DatabaseTest
from test.s2agr.helpers.samples import paper_01_id, paper_02_id, author_01_id

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGTestCase(DatabaseTest):
    def setUp(self) -> None:
        DatabaseTest.setUp(self)
        self.librarian = Builder().build()

    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_paper(self):
        paper = self.librarian.get_paper(paper_01_id)
        self.check_row_count('paper','paper_id', paper_01_id, 1)
        self.assertEqual(paper.paper_id, paper_01_id)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")
        assert_that(paper.abstract, starts_with("We describe"))
        self.check_row_count('citation','cited_id', paper_01_id, 290)
        self.check_row_count('citation','citing_id', paper_01_id, 27)
        self.check_total_row_count('author',23)
        self.check_row_count('wrote','paper_id', paper_01_id, 23)

    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_author(self):
        author = self.librarian.get_author(author_01_id)
        self.assertEqual(author.author_id, author_01_id)
        self.check_row_count('author', 'author_id', author_01_id, 1)

    @test_vcr.use_cassette
    def test_librarian_retrieves_known_author(self):
        self.librarian.get_author(author_01_id)
        author = self.librarian.get_author(author_01_id)
        self.assertEqual(author.author_id, author_01_id)
        self.check_row_count('author', 'author_id', author_01_id, 1)

    @test_vcr.use_cassette
    def test_librarian_retrieves_multiple_papers(self):
        self.librarian.get_papers(paper_01_id, paper_02_id)
        self.check_total_row_count('paper', 2)
        self.check_total_row_count('wrote', 25)

    @test_vcr.use_cassette
    def test_librarian_retrieves_papers_by_author(self):
        self.librarian.get_author(author_01_id)
        self.librarian.get_authored_papers_by(author_01_id)
        self.check_total_row_count('paper', 22)
        self.check_total_row_count('citation',224)


if __name__ == '__main__':
    unittest.main()
