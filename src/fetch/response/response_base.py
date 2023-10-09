from abc import ABCMeta, abstractmethod
from enum import Enum

"""Response http types"""


class ResponseType(Enum):
    TEXT_HTML = "text/html"
    JSON = "application/json"
    XML = "application/xml"
    BINARY = "application/binary"


"""A base response class. Can be extended to represent multiple popular response types
such as text, json, xml, binary etc"""


class ResponseBase(metaclass=ABCMeta):
    def __init__(self, body, headers, cookie=None):
        self.body = body
        self.headers = headers
        self.cookie = cookie
