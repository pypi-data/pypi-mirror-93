import asyncio
import pytest
from unittest.mock import Mock

from threedi_cmd_statistics.statistics.sessions import ApiStats, CrashedDetail
from threedi_cmd_statistics.models import SessionsOptions
from threedi_cmd_statistics.commands.models import MonthsChoices
from threedi_cmd_statistics.http.clients import async_api_clients
from openapi_client import Configuration
from threedi_cmd_statistics.statistics.tools import check_task_results
from openapi_client.models.inline_response20048 import InlineResponse20048
from openapi_client.models import SimulationStatus
from datetime import datetime
from collections import Counter


def configuration():
    conf = Configuration(
        host="test",
        username="tester",
        api_key={
            "Authorization": f"",
            "refresh": f"",
        },
        api_key_prefix={"Authorization": "Bearer"},
    )
    return conf


@pytest.fixture
def settings_mock():
    settings = Mock()
    settings.configuration = configuration()
    yield settings


@pytest.fixture
def session_options(settings_mock):
    html_export_path = None
    verbose = True
    jan = MonthsChoices("1")
    year = "2020"
    options = SessionsOptions(
        html_export_path, verbose, settings_mock,
        jan, year, None, None, None
    )
    yield options


@pytest.fixture
def sim_status():
    sim_status = SimulationStatus(
        url="test",
        name="finished",
        simulation="test/1",
        simulation_id=1,
        simulation_name="test",
        created=datetime.utcnow(),
        time=58585,
        paused=False,
        detail=None,
        exit_code=1210,
        id=45,
    )
    yield sim_status


@pytest.mark.asyncio
async def test_api_stats(session_options):
    clients = async_api_clients(session_options.settings.configuration)
    async with clients.statuses() as client:
        api_stats = ApiStats(client=client, options=session_options, live=False)
        excl_tasks = await api_stats.get_exclude_exit_code_tasks()
        all_tasks = await api_stats()
    assert len(all_tasks) == 4
    assert len(excl_tasks) == 3


@pytest.fixture()
def statuses_list_future(sim_status):
    future = asyncio.Future()
    resp = InlineResponse20048(count=1, next="", previous="", results=[sim_status])
    future.set_result(resp)
    yield future


@pytest.mark.asyncio
async def test_crashed_details(session_options, sim_status, statuses_list_future):
    client = Mock()
    client.statuses_list.return_value = statuses_list_future
    crashed = CrashedDetail(client=client, options=session_options)
    results = await crashed()
    assert isinstance(results, Counter)
    assert list(results.keys())[0] == 1210
    assert list(results.values())[0] == 1


@pytest.mark.asyncio
async def test_check_no_task_results(session_options):
    clients = async_api_clients(session_options.settings.configuration)
    async with clients.statuses() as client:
        api_stats = ApiStats(client=client, options=session_options, live=False)
        all_tasks = await api_stats()
    results = check_task_results(all_tasks)
    # contains errors, so we expect None
    assert results is None


@pytest.mark.asyncio
async def test_check_task_results(session_options):
    resp = InlineResponse20048(count=1, next="", previous="", results=[1, 2, 3])

    all_tasks = [resp, "test"]
    results = check_task_results(all_tasks)
    # contains errors, so we expect None
    assert results == [1, 2, 3, "test"]


