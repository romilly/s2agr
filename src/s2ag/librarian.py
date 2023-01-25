from s2ag.paper import Paper
from s2ag.researcher import Researcher


class Librarian:
    def __init__(self, researcher: Researcher):
        self.researcher = researcher

    def get_paper(self, pid) -> Paper:
        return self.researcher.get_paper(pid)
