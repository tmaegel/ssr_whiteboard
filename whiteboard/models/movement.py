# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
from typing import Any, Union
import sqlite3

from whiteboard.exceptions import (
    MovementNotFoundError,
    MovementInvalidIdError,
    MovementInvalidNameError,
)
from whiteboard.db import get_db


class Movement():

    def __init__(self, _id: int, _name: str, _equipment_ids: int) -> None:
        self.id = _id
        self.name = _name
        self.equipment_ids = _equipment_ids

    def __str__(self):
        return f'Movement ( id={self.id}, name={self.name} )'

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Movement, None]:
        """Create movement instance based on the query."""
        if query is None:
            return None

        return Movement(
            query['id'],
            query['movement'],  # name=movement
            query['equipmentIds'],
        )

    @staticmethod
    def _validate_id(movement_id: Any) -> None:
        """Validate the movement id."""
        if (movement_id is None or not isinstance(movement_id, int) or
                isinstance(movement_id, bool) or movement_id < 0):
            raise MovementInvalidIdError()

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the movement name."""
        if name is None or not isinstance(name, str):
            raise MovementInvalidNameError()

    @staticmethod
    def get(movement_id: int) -> Movement:
        """Get movement from db by id."""
        Movement._validate_id(movement_id)
        db = get_db()
        result = db.execute(
            'SELECT id, movement, equipmentIds'
            ' FROM table_movements WHERE id = ?',
            (movement_id,)
        ).fetchone()

        movement = Movement._query_to_object(result)
        if movement is None:
            raise MovementNotFoundError(movement_id=movement_id)

        return movement
