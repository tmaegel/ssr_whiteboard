#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

LOG_FORMAT = "%(asctime)s - %(name)10s - %(levelname)7s - %(message)s"
# @todo: Set base on config variable
logging.basicConfig(stream=sys.stdout, format=LOG_FORMAT, level=logging.DEBUG)
logger = logging.getLogger("whiteboard")


def debug(message: str) -> None:
    logger.debug(message)


def info(message: str) -> None:
    logger.info(message)


def warning(message: str) -> None:
    logger.warning(message)


def error(message: str) -> None:
    logger.error(message)
