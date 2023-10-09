from bs4 import BeautifulSoup

from src.fetch.request import SimpleGetRequest
from src.fetch.response import ResponseBase

from .crawler_base import CrawlerBase

"""A simple crawler is implemented to provide request settings and response handling for
our basic use case of url fetching. Can be extended to act as a web crawler while collecting other urls from
the response. In our case it will simply output response body to be saved later in storage"""


class SimpleCrawler(CrawlerBase):
    def __init__(self, name: str, url: str, headers=None):
        super().__init__([url], headers)
        self.name = name

    """In this function a programmer can output several types of objects(only dict implemeted).
    But in case you need to read other links from the webpage you can theoretically create another Request
    object and output it. FetchService should have a feature to add new request(s) to it's queue"""

    def process_response(self, response: ResponseBase):
        soup = BeautifulSoup(response.body, "html.parser")
        return {
            "name": self.name.replace("http://", "").replace("https://", ""),
            "html_body": response.body,
            "links": soup.find_all("a"),
            "images": soup.find_all("img"),
            "full_website_name": self.name,
        }

    """Return initial requests associated with this Crawler. To emulate a test case multiple URLs can be set"""

    def get_requests(self):
        reqs = []
        for url in self.urls:
            reqs.append(SimpleGetRequest(url))

        return reqs

    """Unique crawler ID, now simply domain name"""

    def get_id(self):
        return self.name

    def error_callback(self, exception):
        print(f"Error while fetching {self.urls[0]}: {str(exception)}")
