from abc import ABC, abstractmethod
import logging
from datetime import date


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

    def __init__(self):
        self.infos = []
        self.warnings = []
        self.exceptions = []
        self.debugs = []

    def debug(self, message):
        self.debugs.append(message)

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
        filename = f'{date.today().isoformat()}.log'
        log_format = '%(asctime)s - %(levelname)-7s - %(message)s'
        logging.basicConfig(filename=filename, level=log_level, format=log_format)
        logging.info('started')

    def exception(self, message, exception):
        logging.exception(message, exception)

    def warning(self, message):
        logging.warning(message)

    def info(self, message):
        logging.info(message)

    def debug(self, message):
        logging.debug(message)

