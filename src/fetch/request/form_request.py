from .request_base import RequestBase

""""""


class FormRequest(RequestBase):
    def __init__(self, urls, form_data, headers, cookie=None, meta_info=None):
        form_body = self.gen_form_body(form_data)
        super().__init__(urls, form_body, headers, cookie, meta_info)

    def gen_form_body(self, form_data):
        return ""
