import datetime
import json
import os

from .handler_base import HandlerBase


class HtmlBodySettings:
    def __init__(self, save_path):
        self.save_path = save_path


class HtmlBodyHandler(HandlerBase):
    def __init__(self, settings=None):
        super().__init__(settings)

    def is_applicable(self, crawled_data):
        return "html_body" in crawled_data and "name" in crawled_data

    def apply(self, crawled_data):
        file_name = crawled_data["name"] + ".html"
        with open(os.path.join(self.settings.save_path, file_name), "w") as f:
            f.write(crawled_data["html_body"])
        print(f"Successfully fetched {crawled_data['name']}")
