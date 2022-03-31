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


class Equipment:

    equipment_id = Id()
    name = Name()

    def __init__(
        self, equipment_id: Optional[int] = None, name: Optional[str] = None
    ) -> None:
        self.equipment_id = equipment_id
        self.name = name

    def __str__(self):
        return f"Equipment ( equipment_id={self.equipment_id}, name={self.name} )"

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @property
    def id(self):
        return self.equipment_id

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Equipment, None]:
        """Create equipment instance based on the query."""
        if query is None:
            return None

        return Equipment(
            query["id"],
            query["equipment"],  # name=equipment
        )

    @is_defined(attributes=("equipment_id",))
    def get(self) -> Equipment:
        """
        Get equipment from db by id.

        :return: Equipment object
        :rtype: Equipment
        """
        result = self.db.execute(
            "SELECT id, equipment FROM table_equipment WHERE id = ?",
            (self.equipment_id,),
        ).fetchone()

        equipment = Equipment._query_to_object(result)
        if equipment is None:
            raise NotFoundError(type(self).__name__, self.equipment_id)

        return equipment
