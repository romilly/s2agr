from typing import Set

import requests

from s2ag.citation import CITATION_FIELDS, Citation
from s2ag.monitor import Monitor, MockMonitor
from s2ag.paginator import Paginator
from s2ag.paper import Paper, PAPER_FIELDS
from s2ag.requester import Requester


def citations_url_for(pid) -> str:
    return f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations"




class Researcher:
    def __init__(self, requester: Requester, monitor: Monitor = MockMonitor()):
        self.requester = requester
        self.monitor = monitor

    def get_paper(self, pid) -> Paper:
        return Paper(self.get_paper_json(pid))

    def get_paper_json(self, pid: str) -> dict:
        url = self.paper_url_for(pid)
        return self.requester.get(url)

    @staticmethod
    def paper_url_for(pid: str) -> str:
        return f"https://api.semanticscholar.org/graph/v1/paper/{pid}?fields={PAPER_FIELDS}"

    def get_citations_for(self, pid: str) -> Set[Citation]:
        url = citations_url_for(pid)
        paginator = Paginator(self.requester, url, CITATION_FIELDS)
        json_citations = paginator.contents()
        citations = set()
        for json_citation in json_citations:
            if json_citation['citingPaper']['paperId'] is None:
                title = json_citation['citingPaper'].get('title', '*unkown*')
                self.monitor.warn(f'citation citing {pid} titled {title} has no id')
            else:
                citations.add(Citation.create_from(pid, json_citation))
        return citations
