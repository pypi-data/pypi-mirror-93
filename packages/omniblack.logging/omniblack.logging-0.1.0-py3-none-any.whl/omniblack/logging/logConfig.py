import logging
from sys import stdout
from os import environ


def config(disable_rich=False):
    """
    Configure logging to use a nice format.

    Args:
        disable_rich: Disable the 'rich' library activation.
            This will also disable color output.
            'rich' activation can also disable by the NO_COLOR or
            NO_RICH environment variables.

    """
    handlers = None
    format = '%(levelname)s %(asctime)s: %(message)s'
    rich_disabled = 'NO_RICH' in environ or not disable_rich
    if 'NO_COLOR' not in environ and not rich_disabled:
        try:
            from rich.logging import RichHandler
            from rich.traceback import install
            install()
            # We change the format string when rich is enabled, because
            # it will auto color the level when for us
            format = '%(asctime)s: %(message)s'
            handlers = (
                RichHandler(
                    rich_tracebacks=True,
                    show_time=False,
                ),
            )
        except ImportError:
            # Rich is optional
            pass

    if handlers is None:
        handlers = (logging.StreamHandler(stream=stdout), )

    logging.basicConfig(
        format=format,
        datefmt='%m/%d/%Y %I:%M:%S %p',
        handlers=handlers,
    )
