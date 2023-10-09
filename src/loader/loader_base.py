from abc import ABCMeta, abstractmethod

from src.fetch.request import RequestBase

"""A root loader class"""


class LoaderBase(metaclass=ABCMeta):
    def __init__(
        self,
        request: RequestBase,
        loader_settings: dict,
        error_callback=None,
    ):
        self.request = request
        self.loader_settings = loader_settings
        self.error_callback = error_callback

    @abstractmethod
    async def run(self):
        pass
