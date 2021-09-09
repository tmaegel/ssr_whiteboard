# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
import time
from typing import Any, Optional, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    WorkoutInvalidDatetimeError,
    WorkoutInvalidDescriptionError,
    WorkoutInvalidIdError,
    WorkoutInvalidNameError,
    WorkoutNotFoundError,
)
from whiteboard.models.user import User


class Workout():

    def __init__(self, workout_id: int, user_id: int,
                 name: str, description: str,
                 datetime: Optional[int] = int(time.time())) -> None:
        self.workout_id = workout_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.datetime = datetime

        self._db = get_db()

    def __str__(self):
        return f'Workout ( workout_id={self.workout_id},' \
               f' user_id={self.user_id}, name="{self.name}",' \
               f' datetime={self.datetime} )'

    @property
    def db(self):
        return self._db

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Workout, None]:
        """Create workout instance based on the query."""
        if query is None:
            return None

        return Workout(
            query['id'],  # id=workout_id
            query['userId'],
            query['name'],
            query['description'],
            query['datetime']
        )

    @staticmethod
    def _validate_id(workout_id: Any) -> None:
        """Validate the workout id."""
        if (workout_id is None or not isinstance(workout_id, int) or
                isinstance(workout_id, bool) or workout_id < 0):
            raise WorkoutInvalidIdError()

    @staticmethod
    def _validate_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        _user = User(user_id, None, None)
        _user.get()

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the workout name."""
        if name is None or not isinstance(name, str):
            raise WorkoutInvalidNameError()

    @staticmethod
    def _validate_description(description: Any) -> None:
        """Validate the workout description."""
        if (description is None or not isinstance(description, str)):
            raise WorkoutInvalidDescriptionError()

    @staticmethod
    def _validate_datetime(datetime: Any) -> None:
        """Validate the workout datetime."""
        if (datetime is None or
                not isinstance(datetime, int) or
                isinstance(datetime, bool) or datetime < 0):
            raise WorkoutInvalidDatetimeError()

    @staticmethod
    def exist_workout_id(workout_id: int) -> bool:
        """
        Check if workout with workout id exists by requesting them.

        :param: workout id
        :return: True if workout with workout id exists, otherwise False.
        :rtype: bool
        """
        result = get_db().execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout WHERE id = ?', (workout_id,)

        ).fetchone()

        if result is None:
            return False
        else:
            return True

    def get(self) -> Workout:
        """
        Get workout from db by id.

        :return: Workout object
        :rtype: Workout
        """
        Workout._validate_id(self.workout_id)
        result = self.db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout WHERE id = ?', (self.workout_id,)
        ).fetchone()

        workout = Workout._query_to_object(result)
        if workout is None:
            raise WorkoutNotFoundError(workout_id=self.workout_id)

        return workout

    def add(self) -> int:
        """
        Add new workout to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
        Workout._validate_name(self.name)
        Workout._validate_description(self.description)
        Workout._validate_datetime(self.datetime)
        Workout._validate_user_id(self.user_id)

        self.db.execute(
            'INSERT INTO table_workout'
            ' (userId, name, description, datetime)'
            ' VALUES (?, ?, ?, ?)',
            (self.user_id, self.name, self.description, self.datetime)
        )
        self.db.commit()
        inserted_id = self.db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_workout WHERE userId = ? LIMIT 1',
            (self.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    def update(self) -> bool:
        """
        Update workout in db by id.

        :return: True if workout was updated.
        :rtype: bool
        """
        Workout._validate_name(self.name)
        Workout._validate_description(self.description)
        Workout._validate_datetime(self.datetime)
        Workout._validate_id(self.workout_id)
        Workout._validate_user_id(self.user_id)

        if not Workout.exist_workout_id(self.workout_id):
            raise WorkoutNotFoundError(workout_id=self.workout_id)

        self.db.execute(
            'UPDATE table_workout'
            ' SET name = ?, description = ?, datetime = ?'
            ' WHERE id = ? AND userId = ?',
            (self.name, self.description, int(time.time()),
             self.workout_id, self.user_id,)
        )
        self.db.commit()

        return True

    def remove(self) -> bool:
        """
        Remove workout from db by id.

        :return: True if workout was removed.
        :rtype: bool
        """
        Workout._validate_id(self.workout_id)
        Workout._validate_user_id(self.user_id)

        if not Workout.exist_workout_id(self.workout_id):
            raise WorkoutNotFoundError(workout_id=self.workout_id)

        self.db.execute(
            'DELETE FROM table_workout'
            ' WHERE id = ? AND userId = ?', (self.workout_id, self.user_id,)
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
