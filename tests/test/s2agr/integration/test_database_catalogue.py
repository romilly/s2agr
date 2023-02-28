import unittest

import vcr
from hamcrest import assert_that, equal_to, greater_than

from s2agr.citation import Citation
from s2agr.requester import ThrottledRequester
from s2agr.researcher import WebResearcher
from test.s2agr.helpers.database_test import DatabaseTest

test_vcr = vcr.VCR(
    cassette_library_dir='helpers/cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml')
)


class DatabaseCatalogueTestCase(DatabaseTest):
    @test_vcr.use_cassette
    def test_catalogue_writes_paper(self):
        self.check_total_row_count('paper', 0)
        researcher = WebResearcher(ThrottledRequester(delay=0.001))
        paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = researcher.get_paper(paper_id)
        self.catalogue.write_paper(paper)
        self.check_total_row_count('paper', 1)
        self.check_row_count('paper', 'pdf_url','https://www.aclweb.org/anthology/N18-3011.pdf',1)
        self.catalogue.write_paper(paper)

    def test_catalogue_updates_known_paper(self):
        researcher = WebResearcher(ThrottledRequester(delay=0.001))
        paper_id = '649def34f8be52c8b66281af98ae884c09aef38b'
        paper = researcher.get_paper(paper_id)
        self.catalogue.write_paper(paper)
        original_citation_count = paper.citation_count
        original_updated_timestamp = self.get_updated_timestamp(paper_id)
        updated_citation_count = original_citation_count + 3
        paper.jason_dictionary['citationCount'] = updated_citation_count
        self.catalogue.write_paper(paper)
        paper = self.catalogue.read_paper(paper_id)
        assert_that(paper.citation_count, equal_to(updated_citation_count))
        new_updated_timestamp = self.get_updated_timestamp(paper_id)
        assert_that(new_updated_timestamp, greater_than(original_updated_timestamp))

    def get_updated_timestamp(self, paper_id):
        return list(self.catalogue.query(
            'select updated from paper where paper_id=(%s)', (paper_id,)))[0][0]

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
