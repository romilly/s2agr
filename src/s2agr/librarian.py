import psycopg2

from s2agr.citation import Citation
from s2agr.monitor import Monitor
from s2agr.entities import Paper, Author
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.database_catalogue import DatabaseCatalogueException
from s2agr.requester import ThrottledRequesterException
from s2agr.researcher import WebResearcher


class Librarian:
    def __init__(self,
                 researcher: WebResearcher,
                 catalogue: Catalogue,
                 monitor: Monitor):
        self.researcher = researcher
        self.catalogue = catalogue
        self.monitor = monitor

    def get_paper(self, paper_id) -> Paper:
        try:
            if self.catalogue.knows_paper(paper_id):
                paper = self.catalogue.read_paper(paper_id)
            else:
                self.monitor.info('downloading paper %s' % paper_id)
                paper = self.researcher.get_paper(paper_id)
                self.catalogue.write_paper(paper)
                citations = self.researcher.get_citations_for(paper_id)
                for citation in citations:
                    self.catalogue.write_citation(citation)
                references = self.researcher.get_references_for(paper_id)
                for reference in references:
                    self.catalogue.write_citation(reference)
                authors = (Author(ajd) for ajd in paper.authors)
                for author in authors:
                    self.catalogue.write_author(author)
                    self.catalogue.write_wrote(paper_id, author.author_id)

            return paper
        except ThrottledRequesterException as e:
            self.monitor.exception('Could not retrieve paper %s' % paper_id, e)
        except DatabaseCatalogueException as e:
            self.monitor.exception('Database error handling paper %s' % paper_id, e)

    def get_author(self, aid):
        try:
            if self.catalogue.knows_author(aid):
                author = self.catalogue.read_author(aid)
            else:
                self.monitor.info('downloading author %s' % aid)
                author = self.researcher.get_author(aid)
                self.catalogue.write_author(author)
            return author
        except ThrottledRequesterException as e:
            self.monitor.exception('Could not retrieve author %s' % aid, e)
        except psycopg2.Error as e:
            self.monitor.exception('Database error handling author %s' % aid, e)

    def get_papers(self, *paper_ids):
        new_pids = []
        for pid in paper_ids:
            if not self.catalogue.knows_paper(pid):
                new_pids.append(pid)
        new_papers = self.researcher.get_papers(*new_pids)
        for paper in new_papers:
            try:
                self.add_paper_and_attributions(paper)
            except psycopg2.Error as e:
                self.monitor.exception('Database error handling paper %s' % paper.paper_id, e)
                continue
        return (self.catalogue.read_paper(pid) for pid in paper_ids)

    def add_paper_and_attributions(self, paper):
        self.catalogue.write_paper(paper)
        authors = (Author(ajd) for ajd in paper.authors)
        for author in authors:
            self.catalogue.write_wrote(paper.paper_id, author.author_id)

    def get_authored_papers_by(self, author_id: str, lazy=True):
        papers = self.researcher.get_authored_papers_by(author_id)
        for paper in papers:
            if lazy and self.catalogue.knows_paper(paper.paper_id):
                continue
            try:
                self.monitor.debug('adding paper %s' % paper.paper_id)
                self.add_paper_and_attributions(paper)
                self.add_citations_and_references(paper)
            except psycopg2.Error as e:
                self.monitor.exception('Database error handling paper %s' % paper.paper_id, e)
                continue

    def add_citations_and_references(self, paper):
        citations = (Citation(paper.paper_id, cj['paperId'], cj['title']) for cj in paper.citations)
        for citation in citations:
            if citation.citing_id is None:
                self.monitor.warning('null paper id found in citations of %s' % paper.paper_id)
                continue
            self.catalogue.write_citation(citation)
        # references = Citation(cj['paperId'], cj['title']) for cj in paper.ref








