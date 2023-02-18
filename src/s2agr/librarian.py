import psycopg2

from s2agr.monitor import Monitor
from s2agr.entities import Paper, Author
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.database_catalogue import DatabaseCatalogueException
from s2agr.requester import ThrottledRequesterException
from s2agr.researcher import Researcher





class Librarian:
    def __init__(self, 
                 researcher: Researcher,
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






