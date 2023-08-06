import asyncio
from collections import Counter
from threedi_cmd_statistics.http.clients import async_api_clients
from typing import Optional, List
import logging

from openapi_client import ApiException
from openapi_client.models import SimulationStatus, SimulationStatusStatistics
from threedi_cmd_statistics.http.tools import calculate_pagination_offsets
from threedi_cmd_statistics.console import console

from openapi_client.api.statuses_api import StatusesApi
from threedi_cmd_statistics.statistics.tools import check_task_results, StatusMessages
from threedi_cmd_statistics.models import SessionsOptions
from threedi_cmd_statistics.logger import get_logger

SESSION_CNT_DEFS = "crashed,finished,initialized"


EXCLUDE_EXIT_CODES = [2110, 2210, 4264]

logger = get_logger()


def _get_exit_code_counter(results: List[SimulationStatus]) -> Counter:
    return Counter(
        [
            x.exit_code
            for x in results
            if x.exit_code not in EXCLUDE_EXIT_CODES
        ]
    )


def correct_count(
    status_results: List[List[SimulationStatusStatistics]],
) -> List[SimulationStatusStatistics]:
    stats = status_results.pop(0)
    for tr in status_results:
        if not tr:
            continue

        cnt = tr[0].total
        for stat in stats:
            if stat.name == "crashed":
                stat.total -= cnt
            elif stat.name == "finished":
                stat.total += cnt

    return stats


class BaseFetcher:
    def __init__(self, client, options):
        self.options = options
        self.client = client


class ApiStats(BaseFetcher):

    def __init__(self, client, options, live):
        super().__init__(client, options)
        self.live = live

    async def __call__(self):
        all_tasks = []
        loop = asyncio.get_event_loop()
        kwargs = self.options.kwargs.copy()
        if self.live is not None:
            kwargs["simulation__type__live"] = self.live
        stats_task = loop.create_task(
            self.client.statuses_overview(**kwargs)
        )
        all_tasks.append(stats_task)
        extra_tasks = await self.get_exclude_exit_code_tasks()
        all_tasks.extend(extra_tasks)
        task_results = await asyncio.gather(
            *all_tasks, return_exceptions=True
        )
        return task_results

    async def get_exclude_exit_code_tasks(self) -> List[asyncio.Task]:
        tasks = []
        for exit_code in EXCLUDE_EXIT_CODES:
            new_kwargs = self.options.kwargs.copy()
            new_kwargs["exit_code"] = exit_code
            if self.live is not None:
                new_kwargs["simulation__type__live"] = self.live
            t = asyncio.create_task(self.client.statuses_overview(**new_kwargs))
            tasks.append(t)
        return tasks


class CrashedDetail(BaseFetcher):

    def __init__(self, client, options):
        super().__init__(client, options)

    async def __call__(self):
        resp = await self._initial_api_call()
        if not resp:
            return

        if not resp.next:
            return _get_exit_code_counter(resp.results)

        task_results = await self._api_pages(resp)
        if results := check_task_results(task_results, self.options.verbose):
            return _get_exit_code_counter(results)
        return []

    async def _api_pages(self, resp):
        offsets = calculate_pagination_offsets(resp.count)
        tasks = []
        for offset in offsets:
            kwargs_copy = self.options.status_crashed_kwargs.copy()
            kwargs_copy["offset"] = offset
            fetch_task = asyncio.create_task(
                self.client.statuses_list(**kwargs_copy)
            )
            tasks.append(fetch_task)
        task_results = await asyncio.gather(
            *tasks, return_exceptions=True
        )
        return task_results

    async def _initial_api_call(self):
        base_kwargs = self.options.status_crashed_kwargs
        try:
            resp = await self.client.statuses_list(**base_kwargs)
        except ApiException as err:
            if self.options.verbose:
                logger.exception()
            logger.error(f"{err}")
            return

        if not resp:
            logger.info("No results found, filters were %s ", base_kwargs)
            return

        return resp


class Sessions:
    def __init__(
        self,
        options: SessionsOptions,
        live: Optional[bool] = None
    ):
        self.options = options
        self.live = live
        if self.options.verbose:
            logger.level = logging.INFO
        self.clients = async_api_clients(options.settings.configuration)

    async def get_crashed_details(self):
        async with self.clients.statuses() as client:
            crashed_details = CrashedDetail(client, self.options)
            results = await crashed_details()
        return results

    async def get_statistics(
        self,
    ) -> Optional[List[SimulationStatusStatistics]]:
        clients = async_api_clients(self.options.settings.configuration)
        async with clients.statuses() as client:
            api_stats = ApiStats(client=client, options=self.options, live=self.live)
            task_results = await api_stats()
        if results := check_task_results(task_results, self.options.verbose):
            return correct_count(results)
        return []
