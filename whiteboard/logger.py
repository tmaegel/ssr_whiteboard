# -*- coding: utf-8 -*-
import logging
import sys

LOG_FORMAT = '%(asctime)s - %(name)10s - %(levelname)7s - %(message)s'
# @todo: Set base on config variable
logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger('whiteboard')


def debug(message: str):
    logger.debug(f'{message}')


def info(message: str):
    logger.info(f'{message}')


def warning(message: str):
    logger.warning(f'{message}')


def error(message: str):
    logger.error(f'{message}')
