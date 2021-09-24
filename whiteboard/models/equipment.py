# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

from typing import Any, Union
from whiteboard.db import get_db
from whiteboard.exceptions import (
    EquipmentInvalidIdError,
    EquipmentInvalidNameError,
    EquipmentNotFoundError,
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
    Decorator to validate a equipment object.

    :param attr: Attributes of the equipment  object to validate.
                 Possible values: id, name
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'name' in attr:
                _validate_equipment_name(args[0].name)
            if 'id' in attr:
                _validate_equipment_id(args[0].equipment_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_equipment_id(equipment_id: Any) -> None:
        """Validate the equipment id."""
        logger.debug('Validate equipment id.')
        if equipment_id is None or isinstance(equipment_id, bool):
            raise EquipmentInvalidIdError()
        try:
            equipment_id = int(equipment_id)
        except (ValueError, TypeError):
            raise EquipmentInvalidIdError()
        if equipment_id < 0:
            raise EquipmentInvalidIdError()

    def _validate_equipment_name(name: Any) -> Any:
        """Validate the equipment name."""
        logger.debug('Validate equipment name.')
        if name is None or not isinstance(name, str):
            raise EquipmentInvalidNameError()

    return _decorator


class Equipment():

    def __init__(self, equipment_id: int, name: str) -> None:
        self.equipment_id = equipment_id
        self.name = name

    def __str__(self):
        return (f'Equipment ( equipment_id={self.equipment_id},'
                f' name={self.name} )')

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Equipment, None]:
        """Create equipment instance based on the query."""
        if query is None:
            return None

        return Equipment(
            query['id'],
            query['equipment'],  # name=equipment
        )

    @validate(attr=('id'))
    def get(self) -> Equipment:
        """
        Get equipment from db by id.

        :return: Equipment object
        :rtype: Equipment
        """
        result = self.db.execute(
            'SELECT id, equipment FROM table_equipment'
            ' WHERE id = ?', (self.equipment_id,)
        ).fetchone()

        equipment = Equipment._query_to_object(result)
        if equipment is None:
            raise EquipmentNotFoundError(equipment_id=self.equipment_id)

        return equipment
