import unittest

import vcr

from s2ag.researcher import Researcher, Retriever
from s2ag.retriever import WebRetriever

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)

class ResearcherTestCase(unittest.TestCase):

    @test_vcr.use_cassette
    def test_researcher_can_get_paper_using_api(self):
        pid = '649def34f8be52c8b66281af98ae884c09aef38b'
        researcher = Researcher(WebRetriever())
        paper = researcher.get_paper(pid)
        self.assertEqual(paper.paper_id, pid)


if __name__ == '__main__':
    unittest.main()
