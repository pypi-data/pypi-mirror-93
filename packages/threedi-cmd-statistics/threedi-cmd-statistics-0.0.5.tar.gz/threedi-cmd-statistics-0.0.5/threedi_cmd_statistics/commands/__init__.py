import time
from pathlib import Path
from typing import Optional

from threedi_cmd_statistics.console import console

t0 = time.time()


def exit_handler(export_path: Optional[Path]):
    t1 = time.time()
    exec_t = t1 - t0
    if export_path:
        if console.record:
            console.save_html(export_path)
            console.print(f"The command output has been saved to {export_path}")
        else:
            console.print(
                f"Will not save HTML {export_path} because the command did not yield "
                f"any results or session has not been recorded.",
                style="warning",
            )

    console.print(f"[dim light_cyan1]// Execution time {exec_t:.4f} //")
