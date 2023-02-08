import json
import unittest

import vcr

from s2agr.citation import Citation
from s2agr.requester import ThrottledRequester
from s2agr.researcher import Researcher
from test.s2agr.helpers import samples
from test.s2agr.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class DatabaseCatalogueTestCase(DatabaseTest):
    @test_vcr.use_cassette
    def test_catalogue_writes_paper(self):
        self.check_total_row_count('paper', 0)
        researcher = Researcher(ThrottledRequester(delay=0.001))
        paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = researcher.get_paper(paper_id)
        self.catalogue.write_paper(paper)
        self.check_total_row_count('paper', 1)

    def test_catalogue_writes_citations(self):
        self.check_total_row_count('citation', 0)
        self.write_sample_citation()
        self.check_total_row_count('citation', 1)

    def write_sample_citation(self):
        citation = Citation('whatever','dontcare','dummy', False)
        self.catalogue.write_citation(citation)

    def test_catalogue_ignores_duplicated_citations(self):
        self.write_sample_citation()
        self.check_total_row_count('citation', 1)
        self.write_sample_citation()
        self.check_total_row_count('citation', 1)



if __name__ == '__main__':
    unittest.main()
