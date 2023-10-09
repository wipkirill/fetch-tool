from pywebcopy import save_webpage

from .handler_base import HandlerBase


class ClonePageHandlerSettings:
    def __init__(self, enabled, save_path):
        self.enabled = enabled
        self.save_path = save_path


class ClonePageHandler(HandlerBase):
    def __init__(self, settings=None):
        super().__init__(settings)

    def is_applicable(self, crawled_data):
        return self.settings.enabled and "full_website_name" in crawled_data

    def apply(self, crawled_data):
        kwargs = {}

        save_webpage(
            # url of the website
            url=crawled_data["full_website_name"],
            # folder where the copy will be saved
            project_folder=self.settings.save_path,
            **kwargs
        )
