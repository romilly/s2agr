import json

from s2agr.entities import Paper
from s2agr.webresearcher import Researcher


class MockResearcher(Researcher):
    def get_papers(self, *paper_ids):
        return (Paper(self._get_paper_json(paper_id)) for paper_id in paper_ids)

    def __init__(self):
        Researcher.__init__(self)
        self.paper_contents = {}

    def add_paper(self, paper: Paper):
        self.paper_contents[paper.paper_id] = paper.jason_dictionary

    def _get_paper_json(self, pid):
        return self.paper_contents[pid]



