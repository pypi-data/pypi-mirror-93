from functools import lru_cache
import logging
from rich.logging import RichHandler
from threedi_cmd_statistics.console import console


def install_rich_tracebacks():
    from rich.traceback import install
    install(console=console)


@lru_cache()
def get_logger(verbose: bool = False):
    install_rich_tracebacks()

    if verbose:
        level = logging.INFO
    else:
        level = logging.ERROR

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )

    logger = logging.getLogger("rich")
    return logger
