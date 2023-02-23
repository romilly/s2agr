import unittest

import vcr
from hamcrest import assert_that, equal_to, greater_than

from s2agr.requester import ThrottledRequester
from s2agr.researcher import WebResearcher
from s2agr.urls import q
from test.s2agr.helpers.samples import paper_01_id, paper_02_id, author_01_id, author_02_id

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class ResearcherTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.researcher = WebResearcher(ThrottledRequester(delay=0.001))

    @test_vcr.use_cassette
    def test_researcher_can_get_paper_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = self.researcher.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)

    @test_vcr.use_cassette
    def test_researcher_gets_all_author_data_from_paper(self):
        paper = self.researcher.get_paper('d23508ee81467dff9435d42d1d4633e178e59992')
        authors = paper.authors
        author = authors[0]
        assert_that('paperCount' in author.keys())
        assert_that(author['paperCount'], equal_to(43))
        assert_that('hIndex' in author.keys())

    @test_vcr.use_cassette
    def test_researcher_can_get_citations_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        citations = self.researcher.get_citations_for(pid)
        assert_that(len(citations), equal_to(288))
        influential_citations = list(citation for citation in citations if citation.is_influential)
        assert_that(len(influential_citations), equal_to(33))

    @test_vcr.use_cassette
    def test_researcher_can_get_citations_using_new_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        citations = self.researcher.get_citations_for(pid)
        assert_that(len(citations), equal_to(289))
        influential_citations = list(citation for citation in citations if citation.is_influential)
        assert_that(len(influential_citations), equal_to(34))

    @test_vcr.use_cassette
    def test_can_get_papers_satisfying_query(self):
        query = q().with_keywords('temporal','knowledge','graph','embedding').between(2019,2020)
        response = self.researcher.search_by_keyword(query)
        papers = list(response)
        assert_that(len(papers), greater_than(1000))

    @test_vcr.use_cassette
    def test_can_retrieve_multiple_papers(self):
        papers = self.researcher.get_papers(paper_01_id, paper_02_id)
        assert_that(len(list(papers)), equal_to(2))
        test_vcr.use_cassette

    @test_vcr.use_cassette
    def test_can_retrieve_multiple_authors(self):
        ids = (author_01_id, author_02_id)
        authors = list(self.researcher.get_authors(*ids))
        assert_that(len(authors), equal_to(2))




if __name__ == '__main__':
    unittest.main()
