#! coding=utf-8
import logging
import coloredlogs

from pear.utils.config import LOGGING_FORMATTER, IS_DEBUG

logging.basicConfig(format=LOGGING_FORMATTER, level=logging.INFO)
logger = logging.getLogger('')
if not IS_DEBUG:
    logger_handler = logging.FileHandler('log')
    logger_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(LOGGING_FORMATTER)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)

coloredlogs.install(level='INFO', logger=logger, fmt=LOGGING_FORMATTER)
