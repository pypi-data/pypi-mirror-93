import asyncio
from concurrent.futures import CancelledError
from pathlib import Path
from typing import List

import typer
from openapi_client.models.contract import Contract
from threedi_cmd_statistics.statistics.customers import Customers
from threedi_cmd_statistics.statistics.sessions import Sessions
from threedi_cmd_statistics.plots.rich.sessions import (
    plot_sessions,
)
from threedi_cmd_statistics.plots.rich.exit_codes import plot_exit_codes
from threedi_cmd_statistics.plots.rich.customers import plot_customers

from threedi_cmd_statistics.commands.callbacks import HtmlExportPathOption
from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.statistics.usage import Usage
from threedi_cmd_statistics.plots.rich.usage import (
    plot_usage,
)
from threedi_cmd_statistics.statistics.tools import StatusMessages
from threedi_cmd_statistics.commands.callbacks import stats_callback
from threedi_cmd_statistics.logger import get_logger
from threedi_cmd_statistics.models import CustomerOptions

statistics_app = typer.Typer(callback=stats_callback)
customers_app = typer.Typer()


class SessionTasks:

    def __init__(
        self, ctx:
        typer.Context,
        show_crash_details: bool,
        organisation_uid: str = "",
        organisation_name: str = ""
    ):
        """if organisation is given it overwrites the organisation filter on the SessionsOptions instance"""
        self.ctx = ctx
        self.show_crash_details = show_crash_details
        self.ctx.obj.organisation_filter = organisation_uid
        self.organisation_name = organisation_name
        self.tasks = []

    def __call__(self):
        self._collect_tasks()
        self._run_tasks()

    def _collect_tasks(self):
        loop = asyncio.get_event_loop()
        all_sessions = Sessions(self.ctx.obj)
        live_sessions = Sessions(self.ctx.obj, live=True)
        self.tasks = [
            loop.create_task(all_sessions.get_statistics()),
            loop.create_task(live_sessions.get_statistics())
        ]
        if self.show_crash_details:
            self.tasks .append(
                loop.create_task(all_sessions.get_crashed_details())
            )

    def _run_tasks(self):
        logger = get_logger(self.ctx.obj.verbose)
        loop = asyncio.get_event_loop()
        record = bool(self.ctx.obj.html_export_path)

        try:
            results = loop.run_until_complete(asyncio.gather(*self.tasks))
        except CancelledError as err:
            logger.error(f"The operation has been cancelled: {err}")
            results = []

        if not results or not results[0]:
            console.print("No sessions statistics found.", style="warning")
            return
        organisation = self.organisation_name if self.organisation_name else self.ctx.obj.organisation_filter
        plot_sessions(
            results[0], results[1], self.ctx.obj.month,
            self.ctx.obj.year, self.ctx.obj.dates,
            self.ctx.obj.user_filter, organisation, record
        )
        if self.show_crash_details and len(results) > 2:
            plot_exit_codes(results[2])


class UsageTasks:

    def __init__(self, ctx: typer.Context, organisation_uid: str = "", organisation_name: str = ""):
        self.ctx = ctx
        self.ctx.obj.organisation_filter = organisation_uid
        self.organisation_name = organisation_name
        self.tasks = []

    def __call__(self):
        self._collect_tasks()
        self._run_tasks()

    def _collect_tasks(self):
        """overwrites the organisation filter on the SessionsOptions instance"""
        loop = asyncio.get_event_loop()
        usage = Usage(self.ctx.obj)
        task = loop.create_task(usage.get_statistics())
        self.tasks.append(task)

    def _run_tasks(self):
        loop = asyncio.get_event_loop()
        record = bool(self.ctx.obj.html_export_path)

        try:
            results = loop.run_until_complete(asyncio.gather(*self.tasks))
        except CancelledError:
            results = None
        if not results or not results[0]:
            base = ":confused: We're sorry but something went wrong."
            if not self.ctx.obj.verbose:
                base += "You can run this command again with the [bold red]--verbose[/bold red] option to get more information"  # noqa
            console.print(base)
            return
        organisation = self.organisation_name if self.organisation_name else self.ctx.obj.organisation_filter
        plot_usage(results[0], self.ctx.obj.period, organisation, record)


def get_active_organisations(ctx):
    loop = asyncio.get_event_loop()
    co = CustomerOptions(ctx.obj.html_export_path, ctx.obj.verbose, ctx.obj.settings, False)
    customers = Customers(co)
    task = loop.create_task(customers.get_statistics())
    results = loop.run_until_complete(task)
    return results


@statistics_app.command()
def sessions(
    ctx: typer.Context,
    show_crash_details: bool = typer.Option(
        False,
        "--crash-details",
        help="Show detailed statistics of crashed sessions, like exit codes",
    ),
):
    """
    Shows session count statistics, like the total amount of sessions.
    Use the given option filters to narrow down the results to a given period of time of for specific user
    or organisation.

    To get a session count for December, 2020:

        $ statistics --year 2020 --month 12 sessions

    Alternatively you can use several --date options to specify a custom period:

        $ statistics --date 2020-2-22 --date 2020-12-24 sessions

    All these results will distinguish between "finished" and "crashed" sessions.

    """
    loop = asyncio.get_event_loop()

    if not ctx.obj.organisation_filter:
        session_tasks = SessionTasks(ctx, show_crash_details)
        session_tasks()
        raise typer.Exit(0)

    if ctx.obj.organisation_filter[0] == "all":
        organisations = get_active_organisations(ctx)
    else:
        organisations = ctx.obj.organisation_filter

    for organisation in organisations:
        if isinstance(organisation, Contract):
            name = organisation.organisation_name
            uid = organisation.organisation
        else:
            uid = organisation
            name = ""
        session_tasks = SessionTasks(ctx, show_crash_details, uid, name)
        session_tasks()
    loop.stop()


@statistics_app.command()
def usage(ctx: typer.Context):
    """
    Shows aggregated calculation time statistics, like the total, average or maximum calculation duration.
    Use the given option filters to narrow down the results to a given period of time of for specific user
    or organisation.

    To get the calculation statistics for December, 2020:

        $ statistics --year 2020 --month 12 usage

    Alternatively you can use several --date options to specify a custom period:

        $ statistics --date 2020-2-22 --date 2020-12-24 usage

    All these results will include the calculation time for all organisations you have
    the run_simulation permission for. To show the same statistics for a single organisation use
    the --organisation-filter

        $ usage --date 2020-2-22 --date 2020-12-24 --organisation-filter <uuid of the organisation>

    """
    loop = asyncio.get_event_loop()
    if not ctx.obj.organisation_filter:
        usage = UsageTasks(ctx)
        usage()
        raise typer.Exit(0)
    if ctx.obj.organisation_filter[0] == "all":
        organisations = get_active_organisations(ctx)
    else:
        organisations = ctx.obj.organisation_filter

    for organisation in organisations:
        if isinstance(organisation, Contract):
            name = organisation.organisation_name
            uid = organisation.organisation
        else:
            uid = organisation
            name = ""
        usage = UsageTasks(ctx, uid, name)
        usage()
    loop.stop()


@customers_app.command()
def customers(
    ctx: typer.Context,
    all_customers: bool = typer.Option(
        False,
        "--all-customers",
        help="Show all customers (that is, not only active ones that have used some of their calucaltion plan",
    ),
    html_export_path: Path = HtmlExportPathOption,
    verbose: bool = typer.Option(
        False,
        help="Show tracebacks and such",
    ),
):
    """only available for admin/root user. The customer list is limited to active customers by default.
    If you want to list all customers use the --all option."""
    loop = asyncio.get_event_loop()
    record = bool(html_export_path)
    options = CustomerOptions(html_export_path, verbose, ctx.obj, all_customers)
    customers = Customers(options)
    try:
        results = loop.run_until_complete(customers.get_statistics())
    except CancelledError:
        results = []
    finally:
        loop.stop()
    if not results:
        console.print(f"No customers found")
        raise typer.Exit(0)

    plot_customers(results, record)
