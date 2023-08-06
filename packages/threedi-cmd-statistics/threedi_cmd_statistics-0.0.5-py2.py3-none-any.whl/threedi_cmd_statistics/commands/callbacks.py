import atexit
from datetime import datetime
from typing import List, Optional
from pathlib import Path

import typer
from threedi_cmd.commands.models import EndpointChoices
from threedi_cmd.commands.settings import (
    Settings,
    EndpointOption,
    get_settings,
)

from threedi_cmd_statistics.commands import exit_handler
from threedi_cmd_statistics.commands.models import MonthsChoices
from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.validators import ValidationError
from threedi_cmd_statistics.validators.models import OptionsValidator
from threedi_cmd_statistics.models import SessionsOptions, UsageOptions


def html_callback(html_export_path: Path):
    atexit.register(exit_handler, export_path=html_export_path)
    return html_export_path


HtmlExportPathOption = typer.Option(
    None,
    exists=False,
    dir_okay=True,
    writable=True,
    resolve_path=True,
    help="Export the command output to a html file.",
    callback=html_callback
)


VerboseOption: bool = typer.Option(
    False,
    help="In case of command failures this will give you more detailed information, "
         "like the underlying tracebacks"
)


def stats_callback(
    ctx: typer.Context,
    endpoint: EndpointChoices = typer.Option(
        EndpointChoices.production, case_sensitive=False
    ),
    month: MonthsChoices = typer.Option(
        None,
        help="Numerical month representation, e.g. 1 for January, 2 for February,..."
             "If used without the --year option the current year will used automatically"
    ),
    year: str = typer.Option(
        None,
        help="Limit the results to a specific year. This option is mutually exclusive with "
             "the --date option."),
    date: Optional[List[datetime]] = typer.Option(
        None,
        help="Statistics since the given date. "
             "Use a second date option to select a custom period of time. ",
    ),
    user_filter: str = typer.Option(
        None,
        help="Filter by user name, e.g <user>.<name>"
    ),
    organisation_filter: Optional[List[str]] = typer.Option(
        None, help="Filter by organisation uuid, e.g. <78f5a464c35044c19bc7d4b42d7f43dc> "
                   "You can supply multiple organisations by specifying this option multiple times. "
                   "Use 'all' to automatically get results for all active organisations"
    ),
    html_export_path: Path = HtmlExportPathOption,
    verbose: bool = VerboseOption,
):
    """default: 3Di statistics since the beginning of the 3Di era"""
    options_validator = OptionsValidator(
        month, year, date, user_filter, organisation_filter
    )
    try:
        options_validator.validate()
    except ValidationError as err:
        console.print(f"{err}", style="error")
        raise typer.Exit(1)
    endpoint_name = EndpointOption[endpoint.value].name
    settings = get_settings(endpoint_name)

    if ctx.invoked_subcommand == 'sessions':
        options = SessionsOptions(
            html_export_path, verbose, settings, month, year, date, user_filter, organisation_filter
        )
    elif ctx.invoked_subcommand == 'usage':
        options = UsageOptions(
            html_export_path, verbose, settings, month, year, date, user_filter, organisation_filter)
    else:
        return
    ctx.obj = options
    ctx.call_on_close(Settings.save_settings)
