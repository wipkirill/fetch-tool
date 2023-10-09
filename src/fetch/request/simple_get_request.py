from .request_base import RequestBase, RequestMethod

"""A simple get request class. Can be used to fetch webpages without using
any headers. Can be extended to read headers as well"""


class SimpleGetRequest(RequestBase):
    def __init__(self, url, meta_info=None):
        super().__init__([url], None, RequestMethod.GET, None, None, meta_info)

    def get_id(self):
        return self.urls[0]
