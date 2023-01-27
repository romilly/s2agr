import unittest

import vcr
from hamcrest import assert_that, starts_with

from s2ag.librarian import Librarian, Researcher
from s2ag.persistence.database_catalogue import DatabaseCatalogue, test_connection
from s2ag.requester import WebRequester

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class S2AGTestCase(unittest.TestCase):

    @test_vcr.use_cassette
    def test_librarian_retrieves_unknown_paper(self):
        requester = WebRequester()
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        catalogue = DatabaseCatalogue(test_connection())
        librarian = Librarian(Researcher(requester), catalogue)
        paper = librarian.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)
        self.assertEqual(paper.title, "Construction of the Literature Graph in Semantic Scholar")
        assert_that(paper.abstract, starts_with("We describe"))

    # def test_librarian_retrieves_known_paper_from_database(self):
    #     self.fail('not yet implemented')


if __name__ == '__main__':
    unittest.main()
