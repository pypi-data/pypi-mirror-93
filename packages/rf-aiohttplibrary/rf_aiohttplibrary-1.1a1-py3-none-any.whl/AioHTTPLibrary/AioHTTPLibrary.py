# -*- coding: utf-8 -*-

# Copyright (C) 2021 Joshua Kim Rivera

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Created by    : Joshua Kim Rivera
# Date          : January 26 2021 15:09 UTC-8

import asyncio
import aiohttp
import logging
from robot.api import logger
from robot.utils.asserts import fail
from AioHTTPLibrary.version import VERSION

from robotlibcore import (HybridCore,
                          keyword)


__version__ = VERSION

LOGGER = logging.getLogger(__name__)


class AioHTTPLibrary(HybridCore):
    """
    Robotframework Aynschrounous HTTP Library.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        """
        Constructor.
        """
        libraries = []
        HybridCore.__init__(self, libraries)

    @keyword
    def async_get_request(self, urls=[]):
        """
        Performs async calls, then waits for all the responses.
        Returns a dictionary with the url as key containing the response object.

        urls must be a list variable.
        """
        errors = []
        try:
            response = asyncio.run(self.main(urls))
        except Exception as e:
            fail(str(e))
        # logger.console(response)
        data = asyncio.run(self._process_response_to_dict(response))
        # logger.console(data)
        return data

    async def _process_response_to_dict(self, task_returns):
        """
        """
        return_obj = {}
        data = {}
        # logger.console(task_returns)
        for task in task_returns:
            logger.console(task)
            data['status_code'] = task.status
            try:
                data['json'] = await task.json()
            except Exception as e:
                data['json'] = str(e)
            return_obj[str(task.url)] = data
        return dict(return_obj)

    @keyword
    def http_test_urls(self, file, slice=5):
        """
        filename: absolute file path to the file containing the urls.
        slice: whatever
        """
        urls = open(file, "r")
        urls = urls.readlines()
        count = len(urls)
        errors = []
        iter = 0
        hop = slice
        while (iter<=count):
            range = (iter+hop) if ((iter+hop) < count) else count
            logger.console(f"\nInitiating Requests Queue Range {iter}-{range}")
            try:
                results = asyncio.run(self.main(urls[iter:range]))
                for result in results:
                    if (isinstance(result, Exception)):
                        logger.console(result)
                        errors.append(result)
            except Exception as e:
                raise Exception(str(e))
            iter+=hop
        if errors != []:
            raise Exception('\n'.join(map(str, errors)))

    async def get(
        self,
        session: aiohttp.ClientSession,
        url: str,
        iter,
        **kwargs
        ) -> dict:
        """
        Asynchronous get method.
        """
        logger.info(f"Requesting {url}")
        url = url.replace('\n', '')
        resp = None
        try:
            resp = await session.request('GET', url=url, **kwargs)
        except Exception as err:
            raise Exception(str(err) + str(resp.status) + str(url))
        if str(resp.status) != '200':
            raise Exception(str(resp.status) + ' ' + str(url))
        return resp

    async def gather_with_concurrency(self, n, *tasks):
        semaphore = asyncio.Semaphore(n)
        async def sem_task(task):
            async with semaphore:
                return await task
        return await asyncio.gather(*(sem_task(task) for task in tasks))

    async def main(self, urls, **kwargs):
        async with aiohttp.ClientSession() as session:
            tasks = []
            errors = []
            iter = 0
            for url in urls:
                iter+=1
                tasks.append(self.get(session=session, url=url, iter=iter, **kwargs))
            # asyncio.gather() will wait on the entire task set to be
            # completed.  If you want to process results greedily as they come in,
            # loop over asyncio.as_completed()
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            except Exception as e:
                logger.console(str(e))
            return results
