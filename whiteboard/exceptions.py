# -*- coding: utf-8 -*-
import whiteboard.logger as logger


class InvalidAttributeError(Exception):

    """Custom error that raised when a object contains an invalid attribute."""

    def __init__(self, _attr) -> None:
        message = f'Invalid {_attr}.'
        super().__init__(message)
        logger.error(message)


class NotFoundError(Exception):

    """Custom error that raised when a object with an id doesn't exist."""

    def __init__(self, _obj, _id) -> None:
        message = f'{_obj} with id {_id} does not exist.'
        super().__init__(message)
        logger.error(message)


class InvalidPasswordError(Exception):

    """Custom error that raised when a user contains a invalid password."""

    def __init__(self) -> None:
        message = 'Invalid user password.'
        super().__init__(message)
        logger.error(message)
