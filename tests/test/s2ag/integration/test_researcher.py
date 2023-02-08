import unittest

import vcr
from hamcrest import assert_that, equal_to, contains_string, contains, greater_than

from s2ag.queries import q
from s2ag.requester import ThrottledRequester
from s2ag.researcher import Researcher, Requester


test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class ResearcherTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.researcher = Researcher(ThrottledRequester(delay=0.001))

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

# TODO: reinstate when Paginator fixed
#     @test_vcr.use_cassette
#     def test_can_get_papers_satisfying_query(self):
#         query = q().keywords('temporal','knowledge','graph','embedding').between(2019,2020)
#         papers = self.researcher.query(query)
#         assert_that(len(papers), greater_than(1000))


if __name__ == '__main__':
    unittest.main()
