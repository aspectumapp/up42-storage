"""
Standard logger settings
"""

import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
