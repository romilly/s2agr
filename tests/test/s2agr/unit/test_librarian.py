import unittest

from hamcrest import assert_that, equal_to

from s2agr.builder import Builder
from test.s2agr.helpers.mock_catalogue import MockCatalogue
from test.s2agr.helpers.mock_researcher import MockResearcher
from test.s2agr.helpers.samples import paper_01, paper_02, paper_01_id, paper_02_id


class LibrarianTestCase(unittest.TestCase):
    def test_filters_known_papers_from_multiple_paper_request(self):
        catalogue = MockCatalogue()
        catalogue.write_paper(paper_01)
        researcher = MockResearcher()
        researcher.add_paper(paper_02)
        librarian = Builder().with_catalogue(catalogue).with_researcher(researcher).build()
        papers = librarian.get_papers(paper_01_id, paper_02_id)
        assert_that(len(list(papers)), equal_to(2))


if __name__ == '__main__':
    unittest.main()
