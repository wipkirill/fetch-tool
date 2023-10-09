import argparse
import asyncio
import json
import logging
import os

from sys import exit

__title__ = "Fetch"
__version__ = "0.0.1"
__version_info__ = tuple(int(i) for i in __version__.split(".") if i.isdigit())

from src.crawler import SimpleCrawler
from src.fetch.fetch_service import FetchService
from src.handler import (
    ClonePageHandler,
    ClonePageHandlerSettings,
    HtmlBodyHandler,
    HtmlBodySettings,
    MetaHandler,
    MetaHandlerSettings,
)

# def read_settings() -> AgentHostSettings:
#     reader = AgentHostSettingsReader("config.ini")
#     return reader.read_config()


def read_command_line_args():
    parser = argparse.ArgumentParser(description="Process some URLs")
    parser.add_argument(
        "urls", metavar="N", type=str, nargs="*", help="an URL to process", default=[]
    )

    parser.add_argument(
        "-m",
        "--metadata",
        help="Extract meta for this URL",
        type=str,
        required=False,
        default=None,
    )

    parser.add_argument(
        "-c", "--clone", action="store_true", help="Clone webpage with resources"
    )
    args = parser.parse_args()
    return list(set(args.urls)), args.metadata, args.clone


if __name__ == "__main__":
    urls, metadata, clone = read_command_line_args()
    if len(urls) == 0 and metadata is None:
        print("No URLs arg and meta provided, exiting")
        exit(0)

    meta_path = os.path.join(os.getcwd(), "fetch_meta")
    os.makedirs(meta_path, exist_ok=True)
    save_webpage_path = os.path.join(os.getcwd(), "fetch_pages")
    os.makedirs(save_webpage_path, exist_ok=True)

    handlers = [
        MetaHandler(MetaHandlerSettings(meta_path)),
        HtmlBodyHandler(HtmlBodySettings(save_webpage_path)),
        ClonePageHandler(ClonePageHandlerSettings(clone, save_webpage_path)),
    ]
    if metadata:
        meta_handler = handlers[0]
        data = meta_handler.read_meta(metadata)
        if data:
            print("site:", data["site"])
            print("num_links:", data["num_links"])
            print("images:", data["images"])
            print("last_fetch:", data["last_fetch"])
        else:
            print(f"Metadata for {metadata} not found")

    if len(urls) > 0:
        service = FetchService()
        for h in handlers:
            service.add_handler(h)

        for url in urls:
            service.add_crawler(SimpleCrawler(url, url))

        service.add_crawler(None)
        asyncio.run(service.run())
