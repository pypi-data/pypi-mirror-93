import asyncio
from threedi_cmd_statistics.http.clients import async_api_clients
from typing import Optional
import logging

from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.statistics.models import UsageStatisticsResults
from threedi_cmd_statistics.statistics.tools import check_task_results, StatusMessages
from threedi_cmd_statistics.models import UsageOptions
from threedi_cmd_statistics.logger import get_logger

logger = get_logger()


class Usage:
    def __init__(self, options: UsageOptions):
        self.options = options
        if self.options.verbose:
            logger.level = logging.INFO

    async def get_statistics(self) -> Optional[UsageStatisticsResults]:
        clients = async_api_clients(self.options.settings.configuration)
        loop = asyncio.get_event_loop()
        all_tasks = []
        async with clients.usage() as client:
            usage_stats = loop.create_task(
                client.usage_statistics(**self.options.kwargs)
            )
            all_tasks.append(usage_stats)
            kw_live = self.options.kwargs.copy()
            kw_live["simulation__type__live"] = True
            usage_stats_live = loop.create_task(
                client.usage_statistics(**kw_live)
            )
            all_tasks.append(usage_stats_live)
            kw_api = self.options.kwargs.copy()
            kw_api["simulation__type__live"] = False
            usage_stats_api = loop.create_task(
                client.usage_statistics(**kw_api)
            )
            all_tasks.append(usage_stats_api)
            task_results = await asyncio.gather(
                *all_tasks, return_exceptions=True
            )
        if results := check_task_results(task_results, self.options.verbose):
            usage_statistics = UsageStatisticsResults(*results)
            return usage_statistics
