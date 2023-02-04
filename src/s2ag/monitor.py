from abc import ABC, abstractmethod


class Monitor(ABC):
    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def exception(self, message, exception):
        pass

    @abstractmethod
    def warn(self, message):
        pass


class MockMonitor(Monitor):
    def __init__(self):
        self.infos = []
        self.warnings = []
        self.exceptions = []

    def info(self, message):
        self.infos.append(message)

    def warn(self, message):
        self.warnings.append(message)

    def exception(self, message, exception):
        self.exceptions.append([message, exception])


class PrintingMonitor(Monitor):
    def warn(self, message):
        print(message)

    def info(self, message):
        print(message)

    def exception(self, message, exception):
        print(message, exception)