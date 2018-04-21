#! coding=utf-8
import logging
import coloredlogs

from pear.utils.config import LOGGING_FORMATTER, IS_DEBUG

logging.basicConfig(format=LOGGING_FORMATTER, level=logging.INFO)
logger = logging.getLogger('')
coloredlogs.install(level='DEBUG' if IS_DEBUG else 'ERROR', logger=logger, fmt=LOGGING_FORMATTER)
