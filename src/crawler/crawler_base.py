from abc import ABCMeta, abstractmethod

from src.fetch.response import ResponseBase

""" A basic abstract crawler class which is extended by programmers to write their own
request logic and response processing"""


class CrawlerBase(metaclass=ABCMeta):
    def __init__(self, urls, headers=None):
        self.urls = urls
        self.headers = headers

    """Process response. Possible options while parsing: return parsed items or return new requests(more complex web
    crawler scenario)"""

    @abstractmethod
    def process_response(self, response: ResponseBase):
        pass

    """Outputs request object(s)"""

    @abstractmethod
    def get_requests(self):
        pass

    """Unique id"""

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def error_callback(self, exception):
        pass
