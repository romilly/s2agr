from abc import ABC, abstractmethod

from s2ag.citation import Citation
from s2ag.entities import Paper


class Catalogue(ABC):
    @abstractmethod
    def read_paper(self, paper_id: str) -> Paper:
        pass

    @abstractmethod
    def knows(self, item_id: str, table: str, id_col: str):
        pass

    @abstractmethod
    def write_paper(self, paper: Paper):
        pass

    @abstractmethod
    def write_citation(self, citation: Citation):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass

    def knows_paper(self, paper_id: str):
        return self.knows(paper_id, 'paper', 'paper_id')

    def knows_author(self, author_id: str):
        return self.knows(author_id, 'author', 'author_id')

    @abstractmethod
    def read_author(self, aid):
        pass

    @abstractmethod
    def write_author(self, author):
        pass


class NullCatalogue(Catalogue):
    def write_author(self, author):
        pass

    def read_author(self, aid):
        pass

    def write_citation(self, citation):
        pass

    def read_paper(self, paper_id: str) -> Paper:
        pass

    def knows(self, item_id: str, table: str, id_col: str):
        pass

    def write_paper(self, paper: Paper):
        pass


    def close(self):
        pass

    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass
