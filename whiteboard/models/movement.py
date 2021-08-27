# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
from typing import Any, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    MovementInvalidIdError,
    MovementInvalidNameError,
    MovementNotFoundError,
)


class Movement():

    def __init__(self, movement_id: int, name: str,
                 equipment_ids: int) -> None:
        self.movement_id = movement_id
        self.name = name
        self.equipment_ids = equipment_ids

        self._db = get_db()

    def __str__(self):
        return f'Movement ( movement_id={self.movement_id}, name={self.name} )'

    @property
    def db(self):
        return self._db

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

    def get(self) -> Movement:
        """
        Get movement from db by id.

        :return: Movement object
        :rtype: Movement
        """
        Movement._validate_id(self.movement_id)
        result = self.db.execute(
            'SELECT id, movement, equipmentIds'
            ' FROM table_movements WHERE id = ?', (self.movement_id,)
        ).fetchone()

        movement = Movement._query_to_object(result)
        if movement is None:
            raise MovementNotFoundError(movement_id=self.movement_id)

        return movement
