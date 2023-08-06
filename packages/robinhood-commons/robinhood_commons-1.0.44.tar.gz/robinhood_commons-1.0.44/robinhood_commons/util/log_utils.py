import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

from robinhood_commons.log.gzip_rotator import GZipRotator
from robinhood_commons.util.io_utils import ensure_exists

LOGGERS: Dict[str, Logger] = {}


def create_logger(a_path: str) -> Logger:
    """
    Creates a rotating log
    """

    ensure_exists(a_path)

    log_name: str = a_path.split("/")[-1]

    if log_name in LOGGERS:
        return LOGGERS[log_name]

    logger = logging.getLogger(log_name.split(".")[0])
    logger.setLevel(logging.INFO)

    log_handler = TimedRotatingFileHandler(filename=a_path, when="h")

    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    log_handler.rotator = GZipRotator()

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(log_handler)

    LOGGERS[log_name] = logger

    return logger


if __name__ == "__main__":
    from robinhood_commons.util.random_utils import random_float

    path: str = f"/tmp/output/log_utils.{random_float(0, 100)}.log"

    the_logger: Logger = create_logger(a_path=path)
    the_logger.info("help!")

    import os

    os.remove(path=path)
