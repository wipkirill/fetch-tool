import datetime
import json
import os

from .handler_base import HandlerBase


class MetaHandlerSettings:
    def __init__(self, save_path):
        self.save_path = save_path


class MetaHandler(HandlerBase):
    def __init__(self, settings=None):
        super().__init__(settings)

    def is_applicable(self, crawled_data):
        return (
            "name" in crawled_data
            and "links" in crawled_data
            and "images" in crawled_data
        )

    def apply(self, crawled_data):
        file_name = crawled_data["name"].replace("/", "\\") + ".meta"
        with open(os.path.join(self.settings.save_path, file_name), "w") as f:
            now = datetime.datetime.now()
            data = {
                "site": crawled_data["name"],
                "num_links": len(crawled_data["links"]),
                "images": len(crawled_data["images"]),
                "last_fetch": now.strftime("%Y-%m-%d %H:%M:%S"),
            }
            json.dump(data, f)

    def read_meta(self, site_name):
        no_prefix_os_name = (
            site_name.replace("http://", "").replace("https://", "").replace("/", "\\")
            + ".meta"
        )
        if not os.path.exists(os.path.join(self.settings.save_path, no_prefix_os_name)):
            return None
        with open(os.path.join(self.settings.save_path, no_prefix_os_name), "r") as f:
            str_data = f.read()
            return json.loads(str_data)
