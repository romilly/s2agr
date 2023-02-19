from s2agr.librarian import Librarian
from s2agr.monitor import MockMonitor, Monitor
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.database_catalogue import test_connection, DatabaseCatalogue
from s2agr.requester import ThrottledRequester, Requester
from s2agr.webresearcher import WebResearcher


class Builder:
    def __init__(self):
        self.requester = None
        self.researcher = None
        self.connection = None
        self.catalogue = None
        self.monitor = None

    def build(self) -> Librarian:
        if self.requester is None:
            self.requester = ThrottledRequester(delay=0.001)
        if self.monitor is None:
            self.monitor = MockMonitor()
        if self.researcher is None:
            self.researcher = WebResearcher(self.requester, self.monitor)
        if self.connection is None:
            self.connection = test_connection()
        if self.catalogue is None:
            self.catalogue = DatabaseCatalogue(self.connection)
        return Librarian(self.researcher, self.catalogue, self.monitor)

    def with_requester(self, requester: Requester):
        self.requester = requester
        return self

    def with_researcher(self, researcher: WebResearcher):
        self.researcher = researcher
        return self

    def with_catalogue(self, catalogue: Catalogue):
        self.catalogue = catalogue
        return self

    def with_monitor(self, monitor: Monitor):
        self.monitor = monitor
        return self

