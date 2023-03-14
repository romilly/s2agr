from s2agr.citation import Citation
from s2agr.entities import Paper
from s2agr.persistence.catalogue import Catalogue


class MockCatalogue(Catalogue):
    def set_paper_as_linked(self, paper_id):
        pass

    def query(self, sql, values):
        return []

    def __init__(self):
        self._papers = {}

    def read_paper(self, paper_id: str) -> Paper:
        return self._papers[paper_id]

    def knows(self, item_id: str, table: str, id_col: str):
        if table != 'paper':
            raise(NotImplemented('only papers supported atm'))
        return item_id in self._papers

    def write_paper(self, paper: Paper):
        self._papers[paper.paper_id] = paper

    def write_citation(self, citation: Citation):
        pass

    def close(self):
        pass

    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass

    def read_author(self, aid):
        pass

    def write_author(self, author):
        pass

    def write_wrote(self, paper_id, author_id):
        pass
