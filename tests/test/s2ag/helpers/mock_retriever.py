import json

from s2ag.researcher import Retriever


class MockRetriever(Retriever):
    def __init__(self):
        self.papers = {}

    def add_paper(self, pid: str, text: str):
        self.papers[pid] = text



    def get_paper_json(self, pid) -> dict:
        return json.loads(self.papers[pid])
