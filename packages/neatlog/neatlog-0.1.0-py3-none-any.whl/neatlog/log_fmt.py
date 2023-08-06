"""Log formatter"""

import inspect
import logging
import re
from datetime import datetime
from pathlib import PurePosixPath

imported_from_file = inspect.stack(0)[-1].filename
stem = PurePosixPath(imported_from_file).stem


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    black = "\x1b[30m"
    red = "\x1b[31m"
    red_bright = "\x1b[31;1m"
    red_dim = "\x1b[31;2m"
    green = "\x1b[32m"
    green_bright = "\x1b[32;1m"
    green_dim = "\x1b[32;2m"
    yellow = "\x1b[33m"
    yellow_bright = "\x1b[33;1m"
    yellow_dim = "\x1b[33;2m"
    blue = "\x1b[34m"
    blue_bright = "\x1b[34;1m"
    blue_dim = "\x1b[34;2m"
    magenta = "\x1b[35m"
    magenta_bright = "\x1b[35;1m"
    magenta_dim = "\x1b[35;2m"
    cyan = "\x1b[36m"
    cyan_bright = "\x1b[36;1m"
    cyan_dim = "\x1b[36;2m"
    white = "\x1b[37m"
    white_bright = "\x1b[37;1m"
    white_dim = "\x1b[37;2m"
    redyellow = "\x1b[31;43;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt="", prefix="", sep="|", suffix="", color=True):

        if fmt:
            self.fmt = fmt
        else:
            self.fmt = ""
            if prefix:
                self.fmt += f"prefix {sep} "

            self.fmt += f"%(asctime)s {sep} {stem} {sep} %(levelname)-8s {sep} %(message)s (%(filename)s:%(lineno)d)"

            if suffix:
                self.fmt += f" {sep} suffix"

        self.format_colors = {
            logging.DEBUG: self.cyan_bright,
            logging.INFO: self.green,
            logging.WARNING: self.yellow,
            logging.ERROR: self.red_bright,
            logging.CRITICAL: self.redyellow,
        }

        self.formats = {
            logging.DEBUG: self.fmt,
            logging.INFO: self.fmt,
            logging.WARNING: self.fmt,
            logging.ERROR: self.fmt,
            logging.CRITICAL: self.fmt,
        }

        if color:
            for lev in self.formats:
                self.formats[lev] = re.sub(
                    r"(\%\(levelname\))(\S*)",
                    f"{self.format_colors[lev]}\\1\\2{self.reset}",
                    self.fmt,
                )

    def format(self, record):
        _log_fmt = self.white_dim + self.formats.get(record.levelno)
        # print(record.levelno)
        # print(_log_fmt)
        formatter = logging.Formatter(_log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# create stream logging handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(CustomFormatter())

# set overall log level
logging.getLogger().setLevel(logging.DEBUG)


def set_log_level(lev: int):
    for handler in logging.getLogger().handlers:
        handler.setLevel(lev)


def config_logger(log_to_stream=None, log_to_file=None, filename=None):
    logger = logging.getLogger()
    if log_to_stream is not None:
        if log_to_stream:
            logger.addHandler(stream_handler)
        else:
            logger.removeHandler(stream_handler)

    if log_to_file is not None:
        if log_to_file:
            _timestamp = datetime.now().isoformat(timespec="seconds")
            _filename = filename or f"log_{_timestamp}.log"
            file_handler = logging.FileHandler(_filename)
            file_handler.setLevel(logging.WARNING)
            file_handler.setFormatter(CustomFormatter(color=False))
            logger.addHandler(file_handler)
        else:
            for handler in logger.handlers:
                if isinstance(handler, logging.FileHandler):
                    logger.removeHandler(handler)


# default configuration
config_logger(log_to_stream=True, log_to_file=False)

# adjust third party logging
matplotlib_logger = logging.getLogger("matplotlib")
matplotlib_logger.setLevel(level=logging.WARNING)
flake8_logger = logging.getLogger("flake8")
flake8_logger.setLevel(level=logging.ERROR)
filelock_logger = logging.getLogger("filelock")
filelock_logger.setLevel(level=logging.ERROR)
pillow_logger = logging.getLogger("PIL.PngImagePlugin")
pillow_logger.setLevel(level=logging.ERROR)
