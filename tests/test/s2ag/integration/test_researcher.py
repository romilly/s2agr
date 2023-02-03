import unittest

import vcr
from hamcrest import assert_that, equal_to

from s2ag.requester import ThrottledRequester
from s2ag.researcher import Researcher, Requester


test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class ResearcherTestCase(unittest.TestCase):

    @test_vcr.use_cassette
    def test_researcher_can_get_paper_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        researcher = Researcher(ThrottledRequester(delay=0.001))
        paper = researcher.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)

    @test_vcr.use_cassette
    def test_researcher_can_get_citations_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        researcher = Researcher(ThrottledRequester(delay=0.001))
        citations = researcher.get_citations_for(pid)
        assert_that(len(citations), equal_to(286))
        influential_citations = list(citation for citation in citations if citation.is_influential)
        assert_that(len(influential_citations), equal_to(33))


if __name__ == '__main__':
    unittest.main()
