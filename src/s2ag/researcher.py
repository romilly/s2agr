import requests

from s2ag.citation import CITATION_FIELDS, Citation
from s2ag.paginator import Paginator
from s2ag.paper import Paper, PAPER_FIELDS
from s2ag.requester import Requester



class Researcher:
    def __init__(self, requester: Requester):
        self.requester = requester

    def get_paper(self, pid) -> Paper:
        return Paper(self.get_paper_json(pid))

    def get_paper_json(self, pid: str) -> dict:
        url = self.paper_url_for(pid)
        return self.requester.get(url)

    @staticmethod
    def paper_url_for(pid: str) -> str:
        return f"https://api.semanticscholar.org/graph/v1/paper/{pid}?fields={PAPER_FIELDS}"

    def get_citations_for(self, pid: str):
        url = self.citations_url_for(pid)
        paginator = Paginator(self.requester, url, CITATION_FIELDS)
        citations = paginator.contents()
        return list(Citation.create_from(pid, citation) for citation in citations)


    def citations_url_for(self, pid) -> str:
        return f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations"


