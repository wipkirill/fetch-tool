from abc import ABCMeta, abstractmethod

"""Base handler class. Successor classes can check if applicable and work with crawled data. For example
use a metadata crawler to read output of Crawler and write image count, links count etc to disk """


class HandlerBase(metaclass=ABCMeta):
    def __init__(self, settings=None):
        self.settings = settings

    @abstractmethod
    def is_applicable(self, crawled_data):
        pass

    @abstractmethod
    def apply(self, crawled_data):
        pass
