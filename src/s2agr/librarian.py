import psycopg2

from s2agr.monitor import Monitor
from s2agr.entities import Paper, Author
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.database_catalogue import DatabaseCatalogueException
from s2agr.requester import ThrottledRequesterException
from s2agr.webresearcher import WebResearcher





class Librarian:
    def __init__(self,
                 researcher: WebResearcher,
                 catalogue: Catalogue,
                 monitor: Monitor):
        self.researcher = researcher
        self.catalogue = catalogue
        self.monitor = monitor

    def get_paper(self, pid) -> Paper:
        try:
            if self.catalogue.knows_paper(pid):
                paper = self.catalogue.read_paper(pid)
            else:
                self.monitor.info('downloading paper %s' % pid)
                paper = self.researcher.get_paper(pid)
                self.catalogue.write_paper(paper)
                citations = self.researcher.get_citations_for(pid)
                for citation in citations:
                    self.catalogue.write_citation(citation)
                references = self.researcher.get_references_for(pid)
                for reference in references:
                    self.catalogue.write_citation(reference)
                authors = (Author(ajd) for ajd in paper.authors)
                for author in authors:
                    self.catalogue.write_author(author)
                    self.catalogue.write_wrote(paper.paper_id, author.author_id)

            return paper
        except ThrottledRequesterException as e:
            self.monitor.exception('Could not retrieve paper %s' % pid, e)
        except DatabaseCatalogueException as e:
            self.monitor.exception('Database error handling paper %s' % pid, e)

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
            self.add_paper_and_attributions(paper)

        return (self.catalogue.read_paper(pid) for pid in paper_ids)

    def add_paper_and_attributions(self, paper):
        self.catalogue.write_paper(paper)
        authors = (Author(ajd) for ajd in paper.authors)
        for author in authors:
            self.catalogue.write_wrote(paper.paper_id, author.author_id)

    def get_authored_papers_by(self, author_id: str):
        papers = self.researcher.get_authored_papers_by(author_id)
        for paper in papers:
            if self.catalogue.knows_paper(paper.paper_id):
                continue
            self.add_paper_and_attributions(paper)








