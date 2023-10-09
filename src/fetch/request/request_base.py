from abc import ABCMeta, abstractmethod
from enum import Enum

"""Enum of available HTTP request methods"""


class RequestMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


"""A base request class that can be extended to represent a variety of
HTTP requests: GET, POST etc having headers info or other information
describing how to perform request"""


class RequestBase(metaclass=ABCMeta):
    def __init__(
        self,
        urls: [],
        body,
        method: RequestMethod,
        headers: dict = None,
        cookie: dict = None,
        meta_info: dict = None,
    ):
        self.body = body
        self.urls = urls
        self.method = method
        self.headers = headers
        self.cookie = cookie
        self.meta_info = meta_info

    @abstractmethod
    def get_id(self):
        pass
