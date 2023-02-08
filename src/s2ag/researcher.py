from typing import Set

from s2ag.citation import CITATION_FIELDS, Citation
from s2ag.monitor import Monitor, MockMonitor
from s2ag.paginator import Paginator
from s2ag.entities import Paper, PAPER_FIELDS, Author, AUTHOR_FIELDS
from s2ag.queries import q
from s2ag.requester import Requester
from s2ag.urls import UrlBuilder, UrlBuilderForSinglePaper, UrlBuilderForAuthor


def citations_url_for(pid) -> str:
    return f"https://api.semanticscholar.org/graph/v1/paper/{pid}/citations"


def references_url_for(pid) -> str:
    return f"https://api.semanticscholar.org/graph/v1/paper/{pid}/references"


class Researcher:
    def __init__(self, requester: Requester, monitor: Monitor = MockMonitor()):
        self.requester = requester
        self.monitor = monitor

    def get_paper(self, pid) -> Paper:
        return Paper(self.get_paper_json(pid))

    def get_paper_json(self, pid: str) -> dict:
        return self.requester.get(
            self.url_for_paper(pid))

    @staticmethod
    def url_for_paper(pid: str) -> str:
        return UrlBuilderForSinglePaper(pid).with_query(q().with_fields(PAPER_FIELDS)).get_url()

    @staticmethod
    def url_for_author(pid: str) -> str:
        return UrlBuilderForAuthor(pid).with_query(q().with_fields(AUTHOR_FIELDS)).get_url()

    def get_citations_for(self, pid: str) -> Set[Citation]:
        url = citations_url_for(pid)
        paginator = Paginator(self.requester, CITATION_FIELDS, url)
        json_citations = paginator.contents()
        citations = set()
        for json_citation in json_citations:
            if json_citation['citingPaper']['paperId'] is None:
                title = json_citation['citingPaper'].get('title', '*unknown*')
                self.monitor.warning(f'citation citing {pid} titled {title} has no id')
            else:
                citations.add(Citation.create_citation_from(pid, json_citation))
        return citations

    def get_references_for(self, pid: str) -> Set[Citation]:
        url = references_url_for(pid)
        paginator = Paginator(self.requester, CITATION_FIELDS, url)
        json_references = paginator.contents()
        references = set()
        for json_reference in json_references:
            if json_reference['citedPaper']['paperId'] is None:
                title = json_reference['citedPaper'].get('title', '*unknown*')
                self.monitor.warning(f'reference in {pid} titled {title} has no id')
            else:
                references.add(Citation.create_reference_from(pid, json_reference))
        return references

    def get_author(self, aid):
        return Author(self.get_author_json(aid))

    def get_author_json(self, aid):
        return self.requester.get(self.url_for_author(aid))

    def new_get_citations_for(self, pid: str):
        url = citations_url_for(pid)
        # TODO: restore
        # url_generator = UrlBuilder().for_citations_of(pid)
        paginator = Paginator(self.requester, CITATION_FIELDS, url)
        json_citations = paginator.new_contents()
        citations = set()
        for json_citation in json_citations:
            if json_citation['citingPaper']['paperId'] is None:
                title = json_citation['citingPaper'].get('title', '*unknown*')
                self.monitor.warning(f'citation citing {pid} titled {title} has no id')
            else:
                citations.add(Citation.create_citation_from(pid, json_citation))
        return citations
