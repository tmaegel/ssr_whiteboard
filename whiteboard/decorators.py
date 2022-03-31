# -*- coding: utf-8 -*-
from whiteboard import logger
from whiteboard.exceptions import InvalidAttributeError


def is_defined(attributes=()):
    """
    Decorator to check wheather the attributes are defined.

    :param attributes: Attributes of the object to validate.
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            for attr in attributes:
                logger.debug(f"Check if attribute {attr} is defined.")
                if not getattr(args[0], attr):
                    logger.error(f"Attribute {attr} is not defined.")
                    raise InvalidAttributeError(attr)
            return func(*args, **kwargs)

        return _wrapper

    return _decorator
