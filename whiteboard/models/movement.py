#!/usr/bin/env python
# coding=utf-8

# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import json
import sqlite3
from typing import Optional, Union

from whiteboard.db import get_db
from whiteboard.decorators import is_defined
from whiteboard.descriptors import Id, Name
from whiteboard.exceptions import NotFoundError


class Movement:

    movement_id = Id()
    name = Name()
    equipment_ids = Id()

    def __init__(
        self,
        movement_id: Optional[int] = None,
        name: Optional[str] = None,
        equipment_ids: Optional[int] = None,
    ) -> None:
        self.movement_id = movement_id
        self.name = name
        self.equipment_ids = equipment_ids

    def __str__(self):
        return f"Movement ( movement_id={self.movement_id}, name={self.name} )"

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @property
    def id(self):
        return self.movement_id

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Movement, None]:
        """Create movement instance based on the query."""
        if query is None:
            return None

        return Movement(
            query["id"],  # id=movement_id
            query["movement"],  # name=movement
            query["equipmentIds"],
        )

    @is_defined(attributes=("movement_id",))
    def get(self) -> Movement:
        """
        Get movement from db by id.

        :return: Movement object
        :rtype: Movement
        """
        result = self.db.execute(
            "SELECT id, movement, equipmentIds FROM table_movements WHERE id = ?",
            (self.movement_id,),
        ).fetchone()

        movement = Movement._query_to_object(result)
        if movement is None:
            raise NotFoundError(type(self).__name__, self.movement_id)

        return movement
