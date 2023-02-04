import psycopg2

from s2ag.monitor import Monitor
from s2ag.entities import Paper
from s2ag.persistence.catalogue import Catalogue
from s2ag.requester import ThrottledRequesterException
from s2ag.researcher import Researcher


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
            return paper
        except ThrottledRequesterException as e:
            self.monitor.exception('Could not retrieve paper %s' % pid, e)
        except psycopg2.Error as e:
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







