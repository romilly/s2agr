import json
from abc import ABC, abstractmethod

from s2ag.paper import Paper


class Retriever(ABC):
    @abstractmethod
    def get_paper_json(self, pid) -> dict:
        pass


class Researcher:
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def get_paper(self, pid):
        d = self.retriever.get_paper_json(pid)
        # js = '{"paperId": "649def34f8be52c8b66281af98ae884c09aef38b",' \
        #      '"title": "Construction of the Literature Graph in Semantic Scholar"}'
        # d = json.loads(js)
        return Paper(d)


class MockRetriever(Retriever):
    def __init__(self):
        self.papers = {}

    def add_paper(self, pid: str, text: str):
        self.papers[pid] = text



    def get_paper_json(self, pid) -> dict:
        return json.loads(self.papers[pid])


class Librarian:
    def __init__(self, researcher: Researcher):
        self.researcher = researcher

    def get_paper(self, pid) -> Paper:
        return self.researcher.get_paper(pid)
