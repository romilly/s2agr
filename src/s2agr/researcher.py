from typing import Set, List

from abc import ABC, abstractmethod

from s2agr.citation import CITATION_FIELDS, Citation
from s2agr.entities import Paper, EXTENDED_PAPER_FIELDS, Author, AUTHOR_FIELDS, BASE_PAPER_FIELDS, \
    PAPER_FIELDS_WITH_CITATIONS
from s2agr.monitor import Monitor, MockMonitor
from s2agr.paginator import Paginator

from s2agr.requester import Requester
from s2agr.urls import *


class Researcher(ABC):
    def __init__(self, monitor: Monitor = MockMonitor()):
        self.monitor = monitor

    def get_paper(self, pid) -> Paper:
        return Paper(self._get_paper_json(pid))

    @abstractmethod
    def _get_paper_json(self, pid):
        pass

    @abstractmethod
    def get_papers(self, *paper_ids):
        pass


class WebResearcher(Researcher):
    def __init__(self, requester: Requester, monitor: Monitor = MockMonitor()):
        Researcher.__init__(self, monitor)
        self.requester = requester

    def _get_paper_json(self, pid: str) -> dict:
        return self.requester.get(
            self.url_for_paper(pid))

    @staticmethod
    def url_for_paper(pid: str) -> str:
        return UrlBuilderForSinglePaper(pid).with_query(q().with_fields(*EXTENDED_PAPER_FIELDS)).get_url()

    @staticmethod
    def url_for_author(pid: str) -> str:
        return UrlBuilderForAuthor(pid).with_query(q().with_fields(*AUTHOR_FIELDS)).get_url()

    def get_references_for(self, pid: str) -> Set[Citation]:
        paginator = Paginator(self.requester,
                              url_builder=UrlBuilderForPaperReferences(pid).with_query(q().with_fields(*CITATION_FIELDS)))
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
        return Author(self._get_author_json(aid))

    def _get_author_json(self, aid):
        return self.requester.get(self.url_for_author(aid))

    def get_citations_for(self, pid: str):
        paginator = Paginator(self.requester,
                              url_builder=UrlBuilderForPaperCitations(pid).with_query(q().with_fields(*CITATION_FIELDS)))
        json_citations = paginator.contents()
        citations = set()
        for json_citation in json_citations:
            if json_citation['citingPaper']['paperId'] is None:
                title = json_citation['citingPaper'].get('title', '*unknown*')
                self.monitor.warning(f'citation citing {pid} titled {title} has no id')
            else:
                citations.add(Citation.create_citation_from(pid, json_citation))
        return citations

    def search_by_keyword(self, query):
        paginator = Paginator(self.requester,
                        url_builder=UrlBuilderForSearch().with_query(query.with_fields(*BASE_PAPER_FIELDS)), limit=100)
        contents = paginator.contents()
        return contents

    def get_papers(self, *paper_ids):
        url_for_papers = UrlBuilderForPapers().with_query(q().with_fields(*BASE_PAPER_FIELDS)).get_url()
        contents = self.requester.post(url_for_papers, {'ids' : list(paper_ids)})
        return (Paper(paper_json) for paper_json in contents)

    def get_authored_papers_by(self, author_id):
        paginator = Paginator(self.requester,
                              url_builder=UrlBuilderForPapersByAuthor(author_id).with_query(q().with_fields(*PAPER_FIELDS_WITH_CITATIONS)))
        return (Paper(paper_json) for paper_json in paginator.contents())

    def get_authors(self, *author_ids):
        url_for_authors = UrlBuilderForAuthors().with_query(q().with_fields(*AUTHOR_FIELDS)).get_url()
        ids = {'ids': list(author_ids)}
        contents = self.requester.post(url_for_authors, ids)
        return (Author(author_json) for author_json in contents)