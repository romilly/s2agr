from s2ag.paper import Paper
from s2ag.retriever import Retriever


class Researcher:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def get_paper(self, pid):
        return Paper(self.retriever.get_paper_json(pid))
