from abc import ABC, abstractmethod
import logging


class Monitor(ABC):
    @abstractmethod
    def info(self, message):
        pass

    @abstractmethod
    def exception(self, message, exception):
        pass

    @abstractmethod
    def warning(self, message):
        pass

    def debug(self, param):
        pass


class MockMonitor(Monitor):
    def debug(self, param):
        pass

    def __init__(self):
        self.infos = []
        self.warnings = []
        self.exceptions = []

    def info(self, message):
        self.infos.append(message)

    def warning(self, message):
        self.warnings.append(message)

    def exception(self, message, exception):
        self.exceptions.append([message, exception])


class PrintingMonitor(Monitor):
    def warning(self, message):
        print(message)

    def info(self, message):
        print(message)

    def exception(self, message, exception):
        print(message, exception)


class LoggingMonitor(Monitor):
    def __init__(self, log_level=logging.INFO):
        import logging
        logging.basicConfig(filename='production.log', level=log_level)
        logging.info('started')

    def exception(self, message, exception):
        logging.exception(message, exception)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

