# -*- coding: utf-8 -*-
# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

from typing import Any, Union
from whiteboard.db import get_db
from whiteboard.exceptions import (
    MovementInvalidIdError,
    MovementInvalidNameError,
    MovementNotFoundError,
)

import json
import logging
import sqlite3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to logger
handler.setFormatter(formatter)
# add logger
logger.addHandler(handler)


def validate(attr=()):
    """
    Decorator to validate a movement object.

    :param attr: Attributes of the movement  object to validate.
                 Possible values: id, name
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'name' in attr:
                _validate_movement_name(args[0].name)
            if 'id' in attr:
                _validate_movement_id(args[0].movement_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_movement_id(movement_id: Any) -> None:
        """Validate the movement id."""
        logger.debug('Validate movement id.')
        if movement_id is None or isinstance(movement_id, bool):
            logger.error('Invalid movement id.')
            raise MovementInvalidIdError()
        try:
            movement_id = int(movement_id)
        except (ValueError, TypeError):
            logger.error('Invalid movement id.')
            raise MovementInvalidIdError()
        if movement_id < 0:
            logger.error('Invalid movement id.')
            raise MovementInvalidIdError()

    def _validate_movement_name(name: Any) -> Any:
        """Validate the movement name."""
        logger.debug('Validate movement name.')
        if name is None or not isinstance(name, str):
            logger.error('Invalid movement name.')
            raise MovementInvalidNameError()

    return _decorator


class Movement():

    def __init__(self, movement_id: int, name: str,
                 equipment_ids: int) -> None:
        self.movement_id = movement_id
        self.name = name
        self.equipment_ids = equipment_ids

    def __str__(self):
        return f'Movement ( movement_id={self.movement_id}, name={self.name} )'

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Movement, None]:
        """Create movement instance based on the query."""
        if query is None:
            return None

        return Movement(
            query['id'],  # id=movement_id
            query['movement'],  # name=movement
            query['equipmentIds'],
        )

    @validate(attr=('id'))
    def get(self) -> Movement:
        """
        Get movement from db by id.

        :return: Movement object
        :rtype: Movement
        """
        result = self.db.execute(
            'SELECT id, movement, equipmentIds'
            ' FROM table_movements WHERE id = ?', (self.movement_id,)
        ).fetchone()

        movement = Movement._query_to_object(result)
        if movement is None:
            raise MovementNotFoundError(movement_id=self.movement_id)

        return movement
