from s2agr.librarian import Librarian
from s2agr.monitor import MockMonitor, Monitor, LoggingMonitor
from s2agr.persistence.catalogue import Catalogue
from s2agr.persistence.database_catalogue import test_connection, DatabaseCatalogue, production_connection
from s2agr.requester import ThrottledRequester, Requester
from s2agr.researcher import WebResearcher


class Builder:
    def __init__(self):
        self.requester = None
        self.researcher = None
        self.connection = None
        self.catalogue = None
        self.monitor = None

    def build(self) -> Librarian:
        if self.requester is None:
            self.requester = ThrottledRequester()
        if self.monitor is None:
            self.monitor = LoggingMonitor()
        if self.researcher is None:
            self.researcher = WebResearcher(self.requester, self.monitor)
        if self.connection is None:
            self.connection = production_connection()
        if self.catalogue is None:
            self.catalogue = DatabaseCatalogue(self.connection, monitor=self.monitor)
        return Librarian(self.researcher, self.catalogue, self.monitor)

    def build_for_test(self):
        return self.\
            with_requester(ThrottledRequester()).\
            with_monitor(MockMonitor()).\
            with_connection(test_connection()).\
            build()

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

    def with_connection(self, connection):
        self.connection = connection
        return self

