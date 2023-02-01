from abc import ABC, abstractmethod


class Monitor(ABC):
    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def exception(self, message, exception):
        pass


class MockMonitor(Monitor):
    def __init__(self):
        self.messages = []
        self.exceptions = []

    def info(self, message):
        self.messages.append(message)

    def exception(self, message, exception):
        self.exceptions.append([message, exception])