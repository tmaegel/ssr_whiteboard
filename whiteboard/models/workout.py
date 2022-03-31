#!/usr/bin/env python
# coding=utf-8

# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import json
import sqlite3
import time
from typing import Any, Optional, Union

from whiteboard import logger
from whiteboard.db import get_db
from whiteboard.decorators import is_defined
from whiteboard.descriptors import Id, Name, Text, UnixTimestamp
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import User, is_user_exists


def is_workout_exists(func):
    """
    Decorator to check wheather the workout object with id exists.
    :param objects: Objects to be checked for existence.
    """

    def _decorator(*args: Any, **kwargs: Any) -> Any:
        logger.debug("Check if workout exists.")
        try:
            workout_id = getattr(args[0], "workout_id")
        except AttributeError as exc:
            raise InvalidAttributeError("workout_id") from exc
        if not Workout.exist_workout_id(workout_id):
            raise NotFoundError(Workout.__name__, workout_id)
        return func(*args, **kwargs)  # type: ignore

    return _decorator


def is_owner(func):
    """
    Decorator to check wheather the workout is owned by user.
    """

    def _decorator(*args: Any, **kwargs: Any) -> Any:
        # @todo
        return func(*args, **kwargs)  # type: ignore

    return _decorator


class Workout:

    workout_id = Id()
    user_id = Id()
    name = Name()
    description = Text()
    datetime = UnixTimestamp()

    def __init__(
        self,
        workout_id: Optional[int] = None,
        user_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        datetime: Optional[int] = None,
    ) -> None:
        self.workout_id = workout_id
        self.user_id = user_id
        self.name = name
        self.description = description
        if datetime is None:
            self.datetime = int(time.time())
        else:
            self.datetime = datetime

    def __str__(self):
        return (
            f"Workout ( workout_id={self.workout_id},"
            f' user_id={self.user_id}, name="{self.name}",'
            f" datetime={self.datetime} )"
        )

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @property
    def id(self):
        return self.workout_id

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Workout, None]:
        """Create workout instance based on the query."""
        if query is None:
            return None

        return Workout(
            query["id"],  # id=workout_id
            query["userId"],
            query["name"],
            query["description"],
            query["datetime"],
        )

    @staticmethod
    def exist_workout_id(workout_id: int) -> bool:
        """
        Check if workout with workout id exists by requesting them.

        :param: workout id
        :return: True if workout with workout id exists, otherwise False.
        :rtype: bool
        """
        result = (
            get_db()
            .execute("SELECT id FROM table_workout WHERE id = ?", (workout_id,))
            .fetchone()
        )

        if result is None:
            return False

        return True

    @is_defined(attributes=("workout_id", "user_id"))
    @is_user_exists
    def get(self) -> Workout:
        """
        Get workout from db by workout_id and user_id.

        :return: Workout object
        :rtype: Workout
        """
        result = self.db.execute(
            """SELECT id, userId, name, description, datetime
            FROM table_workout WHERE id = ? AND userId = ?""",
            (self.workout_id, self.user_id),
        ).fetchone()

        workout = Workout._query_to_object(result)
        if workout is None:
            raise NotFoundError(type(self).__name__, self.workout_id)

        return workout

    @is_defined(attributes=("user_id", "name", "description", "datetime"))
    @is_user_exists
    def add(self) -> int:
        """
        Add new workout to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
        self.db.execute(
            """INSERT INTO table_workout
            (userId, name, description, datetime)
            VALUES (?, ?, ?, ?)""",
            (self.user_id, self.name, self.description, self.datetime),
        )
        self.db.commit()
        inserted_id = self.db.execute(
            "SELECT last_insert_rowid() FROM table_workout WHERE userId = ? LIMIT 1",
            (self.user_id,),
        ).fetchone()

        try:
            return int(inserted_id["last_insert_rowid()"])
        except (TypeError, ValueError) as e:
            logger.error("Invalid last_insert_rowid: %s" % e)
            raise

    @is_defined(attributes=("workout_id", "user_id", "name", "description", "datetime"))
    @is_workout_exists
    @is_user_exists
    def update(self) -> bool:
        """
        Update workout in db by id.

        :return: True if workout was updated.
        :rtype: bool
        """
        self.db.execute(
            """UPDATE table_workout
            SET name = ?, description = ?, datetime = ?
            WHERE id = ? AND userId = ?""",
            (
                self.name,
                self.description,
                int(time.time()),
                self.workout_id,
                self.user_id,
            ),
        )
        self.db.commit()

        return True

    @is_defined(attributes=("workout_id", "user_id"))
    @is_workout_exists
    @is_user_exists
    def remove(self) -> bool:
        """
        Remove workout from db by id.

        :return: True if workout was removed.
        :rtype: bool
        """
        self.db.execute(
            "DELETE FROM table_workout WHERE id = ? AND userId = ?",
            (
                self.workout_id,
                self.user_id,
            ),
        )
        self.db.commit()
        # @todo
        # Remove Connection between tags and workouts
        # @todo: use current delete_score function
        # db.execute(
        #     'DELETE FROM table_workout_score'
        #     ' WHERE workoutId = ? AND userId = ?',
        #     (workout_id, g.user['id'],)
        # )
        # db.commit()

        return True

    @staticmethod
    def list(
        user_id: int, order_by: str = "name", sort: str = "asc"
    ) -> list[Optional[Workout]]:
        """
        Return a list of all workouts.

        :return: List of all workouts.
        :rtype: list
        """
        # Validate user_id
        _user = User(user_id, None, None)
        _user.get()

        # Include admin (common) workouts
        where_filter = "userId = 1 OR userId = ?"
        results = (
            get_db()
            .execute(
                f"""SELECT id, userId, name, description, datetime
                FROM table_workout
                WHERE ({where_filter})
                ORDER BY {order_by} {sort}""",
                (user_id,),
            )
            .fetchall()
        )

        workouts = []
        for workout in results:
            workouts.append(Workout._query_to_object(workout))

        return workouts
