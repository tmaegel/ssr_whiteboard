# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
from typing import Any, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    EquipmentInvalidIdError,
    EquipmentInvalidNameError,
    EquipmentNotFoundError,
)


class Equipment():

    def __init__(self, equipment_id: int, name: str) -> None:
        self.equipment_id = equipment_id
        self.name = name

        self._db = get_db()

    def __str__(self):
        return (f'Equipment ( equipment_id={self.equipment_id},'
                f' name={self.name} )')

    @property
    def db(self):
        return self._db

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Equipment, None]:
        """Create equipment instance based on the query."""
        if query is None:
            return None

        return Equipment(
            query['id'],
            query['equipment'],  # name=equipment
        )

    @staticmethod
    def _validate_id(equipment_id: Any) -> None:
        """Validate the equipment id."""
        if (equipment_id is None or not isinstance(equipment_id, int) or
                isinstance(equipment_id, bool) or equipment_id < 0):
            raise EquipmentInvalidIdError()

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the equipment name."""
        if name is None or not isinstance(name, str):
            raise EquipmentInvalidNameError()

    def get(self) -> Equipment:
        """
        Get equipment from db by id.

        :return: Equipment object
        :rtype: Equipment
        """
        Equipment._validate_id(self.equipment_id)
        result = self.db.execute(
            'SELECT id, equipment FROM table_equipment'
            ' WHERE id = ?', (self.equipment_id,)
        ).fetchone()

        equipment = Equipment._query_to_object(result)
        if equipment is None:
            raise EquipmentNotFoundError(equipment_id=self.equipment_id)

        return equipment
