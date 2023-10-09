from .request_base import RequestBase, RequestMethod


class PostRequest(RequestBase):
    def __init__(self, urls, body, headers, cookie=None, meta_info=None):
        super().__init__(urls, body, RequestMethod.POST, headers, cookie, meta_info)
