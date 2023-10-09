from .response_base import ResponseBase, ResponseType

"""
A simple text response object is returned after http GET operations
"""


class TextHtmlResponse(ResponseBase):
    def __int__(self, response_body, headers, cookie):
        super().__init__(response_body, headers, cookie)
