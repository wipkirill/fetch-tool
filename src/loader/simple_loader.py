import aiohttp

from src.fetch.request import RequestBase, RequestMethod
from src.fetch.response import TextHtmlResponse

from .loader_base import LoaderBase

"""An HTTP loader implementation based on aiohttp library"""


class SimpleLoader(LoaderBase):
    def __init__(
        self,
        request: RequestBase,
        loader_settings: dict,
        error_callback=None,
    ):
        super().__init__(request, loader_settings, error_callback)

    async def run(self):
        async with aiohttp.ClientSession() as session:
            match self.request.method:
                case RequestMethod.GET:
                    try:
                        async with session.get(self.request.urls[0]) as resp:
                            response = None
                            match resp.content_type:
                                case "text/html":
                                    response = TextHtmlResponse(
                                        await resp.text(), resp.headers, resp.cookies
                                    )
                                case "application/json":
                                    # JSON response type here
                                    pass
                                case "application/xml":
                                    # XML response type here
                                    pass
                            return response

                    except Exception as e:
                        self.error_callback(e)
                        return None
                case RequestMethod.POST:
                    # POST request code
                    pass

        return None
