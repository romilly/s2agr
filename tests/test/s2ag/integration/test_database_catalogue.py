import json
import unittest

import vcr

from s2ag.paper import Paper
from s2ag.requester import WebRequester
from s2ag.researcher import Researcher
from test.s2ag.helpers.database_test import DatabaseTest
from test.s2ag.unit.test_paper_citations import read

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class DatabaseCatalogueTestCase(DatabaseTest):
    @test_vcr.use_cassette
    def test_catalogue_writes_paper(self):
        # TODO: use sample paper instead of Researcher
        self.check_total_row_count('paper', 0)
        researcher = Researcher(WebRequester())
        paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = researcher.get_paper(paper_id)
        self.catalogue.write_paper(paper)
        self.check_total_row_count('paper', 1)

    def test_catalogue_writes_citations(self):
        # TODO: create python files with samples, and import the data directly
        self.check_total_row_count('citation', 0)
        jd = json.loads(read('test/s2ag/data/samples/sample_02.json'))
        paper = Paper(jd)
        citations = paper.get_citation_entries()
        for citation in citations:
            self.catalogue.write_citation(citation)
        self.check_total_row_count('citation', 3)


if __name__ == '__main__':
    unittest.main()
