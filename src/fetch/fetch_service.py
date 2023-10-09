import asyncio
import logging
import traceback

from asyncio import QueueFull

from src.crawler import CrawlerBase
from src.fetch.request import RequestBase, RequestMethod
from src.loader import SimpleLoader


class FetchService:
    def __init__(self):
        self.max_job_queue_size = 100
        self.request_queue = asyncio.Queue(self.max_job_queue_size)
        self._tasks = {}
        self._crawlers = {}
        self._logger = logging.getLogger(__name__)
        self._stop_requested = False
        self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def get_task_queue_size(self):
        """
        Get work queue size

        :return:
        """
        return self.request_queue.qsize()

    def get_unfinished_queue_size(self):
        """
        Get work queue size

        :return:
        """
        return self.request_queue._unfinished_tasks

    def add_crawler(self, crawler: CrawlerBase):
        """This method is used to put task request data to task queue request_queue"""
        try:
            # Termination
            if crawler is None:
                self.request_queue.put_nowait(None)
            else:
                self._crawlers[crawler.get_id()] = crawler
                for r in crawler.get_requests():
                    self.request_queue.put_nowait(r)
        except QueueFull as e:
            raise e
        except Exception as e:
            self._logger.error("An exception occurred: %s", str(e))
            raise e

    async def run(self):
        """Main loop. Requests are taken from request queue and executed one by one"""
        req_id = None
        while not self._stop_requested:
            try:
                self._logger.info("Consumer: waiting for item")
                request = await self.request_queue.get()

                if request is None:
                    # None is the signal to stop.
                    # self._task_request_queue.task_done()
                    self._logger.info("Consumer: exiting")
                    return
                req_id = request.get_id()

                self._logger.info("Consumer: has item %s", req_id)
                assert req_id in self._crawlers
                crawler = self._crawlers[req_id]
                crawl_task = asyncio.create_task(self._run_crawler(request, crawler))
                done, pending = await asyncio.wait(
                    [crawl_task], return_when=asyncio.FIRST_COMPLETED
                )

            except Exception:  # noqa
                self._logger.error(
                    "An unknown at run() exception:" + traceback.format_exc()
                )
            finally:
                self.request_queue.task_done()
        self._logger.info("Consumer: ending")

    async def _run_crawler(self, request: RequestBase, crawler: CrawlerBase):
        try:
            if request.meta_info and "use_cloudfare" in request.meta_info:
                # Use more complex loader here to trick Cloudfare
                return
            if request.meta_info and "use_playwright" in request.meta_info:
                # Use Javascript rendering features here
                return

            # Use simple loader
            loader_settings = {}
            loader = SimpleLoader(
                request, loader_settings, lambda e: crawler.error_callback(e)
            )
            response = await loader.run()
            web_crawler_data = {}
            if response is not None:
                web_crawler_data = crawler.process_response(response)

            for h in self.handlers:
                if h.is_applicable(web_crawler_data):
                    h.apply(web_crawler_data)

        except Exception as ex:
            print(f"An error occurred while fetching {request.urls[0]}: {str(ex)}")
