from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from rich.style import Style
from rich.padding import Padding
from rich.table import Table
from rich import box

from threedi_cmd_statistics.console import console
from threedi_cmd_statistics.commands.models import MonthsChoices

from typing import List
from openapi_client.models import SimulationStatusStatistics


@dataclass
class SessionCount:
    result: List[SimulationStatusStatistics]
    crashed: int = field(init=False)
    finished: int = field(init=False)
    total: int = field(init=False)
    percentage_crashed: int = field(init=False)
    percentage_finished: int = field(init=False)

    def __post_init__(self):
        for stat in self.result:
            setattr(self, stat.name, stat.total)

        if not hasattr(self, "crashed"):
            self.crashed = 0
        if not hasattr(self, "finished"):
            self.finished = 0
        self.total = self.crashed + self.finished
        try:
            self.percentage_crashed = round((self.crashed * 100) / self.total)
        except ZeroDivisionError:
            self.percentage_crashed = 0
        try:
            self.percentage_finished = round(
                (self.finished * 100) / self.total
            )
        except ZeroDivisionError:
            self.percentage_finished = 0


class SessionCountGrids:

    def __init__(
        self,
        session_count_all: SessionCount,
        session_count_live: SessionCount,
        title: str
    ):
        self.session_count = session_count_all
        self.session_count_live = session_count_live
        self.title = title
        self.name_column_width = int((console.width * 6) / 100)
        self.count_column_width = int((console.width * 8) / 100)
        self.type_column_width = int((console.width * 12) / 100)
        self.perc_column_width = int((console.width * 8) / 100)
        self.width_left = (console.width * 50) / 100
        self.crashed_style = Style(bgcolor="red")
        self.finished_style = Style(bgcolor="green")

    def _get_base(self, header=False) -> Table:
        t = self.title if header else None
        grid = Table(
            title=t,
            show_header=header,
            show_lines=False,
            box=box.SIMPLE_HEAD
        )

        grid.add_column(
            "Status",
            width=self.name_column_width,
            justify="left"
        )
        grid.add_column(
            "Count",
            width=self.count_column_width,
            style=Style(color="magenta", bold=True),
            header_style=Style(color="magenta", bold=True),
            justify="left",
        )
        grid.add_column(
            "API/Live",
            width=self.type_column_width,
            style=Style(color="cyan", bold=True),
            header_style=Style(color="cyan", bold=True),
            justify="left",
        )
        grid.add_column(
            "Percent",
            width=self.perc_column_width,
            justify="left",
        )
        return grid

    @property
    def finished_grid(self) -> Table:
        grid = self._get_base(header=True)
        plot_column_width = int(
            (self.width_left * self.session_count.percentage_finished) / 100
        )
        grid.add_column(
            max_width=plot_column_width,
            width=plot_column_width,
            style=self.finished_style,
        )
        grid.add_row(
            "finished",
            f"{self.session_count.finished}",
            f"{self.session_count.finished - self.session_count_live.finished}/{self.session_count_live.finished}",
            f" {self.session_count.percentage_finished}%",
            "",
        )
        return grid

    @property
    def crashed_grid(self) -> Table:
        grid = self._get_base()
        plot_column_width = int(
            (self.width_left * self.session_count.percentage_crashed) / 100
        )
        grid.add_column(
            max_width=plot_column_width,
            width=plot_column_width,
            style=self.crashed_style,
        )
        grid.add_row(
            "crashed",
            f"{self.session_count.crashed}",
            f"{self.session_count.crashed - self.session_count_live.crashed}/{self.session_count_live.crashed}",
            f" {self.session_count.percentage_crashed}%",
            "",
        )
        return grid


def plot_sessions(
    all_sessions: List[SimulationStatusStatistics],
    live_sessions: List[SimulationStatusStatistics],
    month: Optional[MonthsChoices],
    year: Optional[str],
    dates: Optional[List[datetime]],
    user_filter: Optional[str],
    organisation_filter: Optional[str],
    record: bool = False,
) -> None:
    if record:
        console.record = True
    session_count_all = SessionCount(all_sessions)
    session_count_live = SessionCount(live_sessions)
    title = get_title(month, year, dates, user_filter, organisation_filter)
    grids = SessionCountGrids(session_count_all, session_count_live, title)
    console.print(Padding("", (1, 0)))
    console.print(grids.finished_grid)
    console.print(grids.crashed_grid)
    console.print(Padding("", (1, 0)))


def get_title(
    month: Optional[MonthsChoices],
    year: Optional[str],
    dates: Optional[List[datetime]],
    user_filter: Optional[str],
    organisation_filter: Optional[str],
):
    base_str = f"[bold] Session count"
    if month:
        base_str += f" | {month.name}"
    if year:
        base_str += f" | {year}"
    if dates:
        try:
            start_date, end_date = dates
            base_str += f" {start_date} - {end_date}"
        except ValueError:
            base_str += f" since {dates[0]}"
    if user_filter:
        base_str += f" | user {user_filter}"
    if organisation_filter:
        base_str += f" | organisation {organisation_filter}"
    return base_str
