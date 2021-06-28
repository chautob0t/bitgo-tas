import logging
import os

LOGGER_NAME = "parent"


def setup_logger():
    level = logging.DEBUG if os.getenv("DEBUG", False) else logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


setup_logger()


def get_logger(name=None):
    return logging.getLogger(name)
