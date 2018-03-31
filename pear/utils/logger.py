#! coding=utf-8
import logging

from pear.utils.config import LOGGING_FORMATTER

logging.basicConfig(format=LOGGING_FORMATTER, level=logging.INFO)
logger = logging.getLogger('')
