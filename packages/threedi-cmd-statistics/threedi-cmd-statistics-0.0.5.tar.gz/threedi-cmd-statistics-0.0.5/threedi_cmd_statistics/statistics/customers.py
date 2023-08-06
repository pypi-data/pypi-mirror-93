import asyncio
import logging
from typing import List, Optional

from openapi_client.models import Contract
from openapi_client import ApiException
from threedi_cmd_statistics.http.clients import async_api_clients
from threedi_cmd_statistics.http.tools import calculate_pagination_offsets
from threedi_cmd_statistics.statistics.tools import StatusMessages
from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.models import CustomerOptions
from threedi_cmd_statistics.logger import get_logger


logger = get_logger()


class Customers:
    def __init__(self, options: CustomerOptions):
        self.options = options
        if self.options.verbose:
            logger.level = logging.INFO

    async def get_statistics(self) -> List[Optional[Contract]]:
        clients = async_api_clients(self.options.settings.configuration)
        async with clients.contracts() as client:
            try:
                resp = await client.contracts_list(**self.options.kwargs)
            except ApiException as err:
                if self.options.verbose:
                    logger.exception()
                logger.error(f"{err}")
                return []

            if not resp:
                logger.info("No results found, filters were %s ", self.options.kwargs)
                return []

            if not resp.next:
                return resp.results

            offsets = calculate_pagination_offsets(resp.count)
            tasks = []
            for offset in offsets:
                kwargs_copy = self.options.kwargs.copy()
                kwargs_copy["offset"] = offset
                fetch_task = asyncio.create_task(
                    client.contracts_list(**kwargs_copy)
                )
                tasks.append(fetch_task)
            task_results = await asyncio.gather(
                *tasks, return_exceptions=True
            )

        results = []
        for task_result in task_results:
            if isinstance(task_result, Exception):
                logger.error(task_result)
                return []
            results.extend(task_result.results)

        return results
