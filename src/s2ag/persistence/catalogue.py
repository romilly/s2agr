from abc import ABC, abstractmethod
from typing import List

from s2ag.paper import Paper


class Catalogue(ABC):
    @abstractmethod
    def read_paper(self, paper_id: str) -> Paper:
        pass

    @abstractmethod
    def knows(self, id):
        pass

    @abstractmethod
    def write_paper(self, paper: Paper):
        pass

    # @abstractmethod
    # def keys(self) -> List[str]:
    #     pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass

class NullCatalogue(Catalogue):
    def read_paper(self, paper_id: str) -> Paper:
        pass

    def knows(self, id):
        pass

    def write_paper(self, paper: Paper):
        pass

    def close(self):
        pass

    def set_pdf_location(self, paper_id: str, pdf_location: str):
        pass