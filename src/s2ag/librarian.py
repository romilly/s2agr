from s2ag.paper import Paper
from s2ag.persistence.catalogue import Catalogue, NullCatalogue
from s2ag.researcher import Researcher


class Librarian:
    def __init__(self, researcher: Researcher, catalogue: Catalogue):
        self.researcher = researcher
        self.catalogue = catalogue

    def get_paper(self, pid) -> Paper:
        if not self.catalogue.knows(pid):
            paper = self.researcher.get_paper(pid)
            self.catalogue.write_paper(paper)
        return self.catalogue.read_paper(pid)
