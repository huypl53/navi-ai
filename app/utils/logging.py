import logging
from rich.console import Console
from rich.logging import RichHandler


from app.utils.singleton import SingletonMeta

log_formatter = logging.Formatter(
    "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
)

file_handler = logging.FileHandler('./bkt.log')
file_handler.setFormatter(log_formatter)

# console_handler = logging.StreamHandler()
# console_handler.setFormatter(log_formatter)


class RichConsoleHandler(RichHandler):
    def __init__(self, width=200, style=None, **kwargs):
        super().__init__(
            console=Console(color_system="256", width=width, style=style), **kwargs
        )


class AppLogger(metaclass=SingletonMeta):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(RichConsoleHandler())
        self._logger.addHandler(file_handler)

    def get_logger(self):
        return self._logger
