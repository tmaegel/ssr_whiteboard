# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
from typing import Any, Union
import sqlite3

from whiteboard.exceptions import (
    EquipmentNotFoundError,
    EquipmentInvalidIdError,
    EquipmentInvalidNameError,
)
from whiteboard.db import get_db


class Equipment():

    def __init__(self, _id: int, _name: str) -> None:
        self.id = _id
        self.name = _name

    def __str__(self):
        return f'Equipment ( id={self.id}, name={self.name} )'

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

    @staticmethod
    def get(equipment_id: int) -> Equipment:
        """Get equipment from db by id."""
        Equipment._validate_id(equipment_id)
        db = get_db()
        result = db.execute(
            'SELECT id, equipment FROM table_equipment WHERE id = ?',
            (equipment_id,)
        ).fetchone()

        equipment = Equipment._query_to_object(result)
        if equipment is None:
            raise EquipmentNotFoundError(equipment_id=equipment_id)

        return equipment
