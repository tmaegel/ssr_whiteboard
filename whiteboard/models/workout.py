# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

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

import json
import logging
import sqlite3
import time

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
    Decorator to validate a workout object.

    :param attr: Attributes of the workout object to validate.
                 Possible values: id, user_id, name, description, datetime
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'name' in attr:
                _validate_workout_name(args[0].name)
            if 'description' in attr:
                _validate_workout_description(args[0].description)
            if 'datetime' in attr:
                _validate_workout_datetime(args[0].datetime)
            if 'id' in attr:
                _validate_workout_id(args[0].workout_id)
            if 'user_id' in attr:
                _validate_workout_user_id(args[0].user_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_workout_id(workout_id: Any) -> None:
        """Validate the workout id."""
        logger.debug('Validate workout id.')
        if workout_id is None or isinstance(workout_id, bool):
            raise WorkoutInvalidIdError()
        try:
            workout_id = int(workout_id)
        except (ValueError, TypeError):
            raise WorkoutInvalidIdError()
        if workout_id < 0:
            raise WorkoutInvalidIdError()

    def _validate_workout_name(name: Any) -> Any:
        """Validate the workout name."""
        logger.debug('Validate workout name.')
        if name is None or not isinstance(name, str):
            raise WorkoutInvalidNameError()

    def _validate_workout_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        logger.debug('Validate workout user id.')
        _user = User(user_id, None, None)
        _user.get()

    def _validate_workout_description(description: Any) -> None:
        """Validate the workout description."""
        logger.debug('Validate workout description.')
        if (description is None or not isinstance(description, str)):
            raise WorkoutInvalidDescriptionError()

    def _validate_workout_datetime(datetime: Any) -> None:
        """Validate the workout datetime."""
        logger.debug('Validate workout datetime.')

        if datetime is None or isinstance(datetime, bool):
            raise WorkoutInvalidDatetimeError()
        try:
            datetime = int(datetime)
        except (ValueError, TypeError):
            raise WorkoutInvalidDatetimeError()
        if datetime < 0:
            raise WorkoutInvalidDatetimeError()

    return _decorator


class Workout():

    def __init__(self, workout_id: int, user_id: int = None,
                 name: str = None, description: str = None,
                 datetime: Optional[int] = int(time.time())) -> None:
        self.workout_id = workout_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.datetime = datetime

    def __str__(self):
        return f'Workout ( workout_id={self.workout_id},' \
               f' user_id={self.user_id}, name="{self.name}",' \
               f' datetime={self.datetime} )'

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

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

    @validate(attr=('id'))
    def get(self) -> Workout:
        """
        Get workout from db by id.

        :return: Workout object
        :rtype: Workout
        """
        result = self.db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout WHERE id = ?', (self.workout_id,)
        ).fetchone()

        workout = Workout._query_to_object(result)
        if workout is None:
            raise WorkoutNotFoundError(workout_id=self.workout_id)

        return workout

    @validate(attr=('user_id', 'name', 'description', 'datetime'))
    def add(self) -> int:
        """
        Add new workout to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
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

    @validate(attr=('id', 'user_id', 'name', 'description', 'datetime'))
    def update(self) -> bool:
        """
        Update workout in db by id.

        :return: True if workout was updated.
        :rtype: bool
        """
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

    @validate(attr=('id', 'user_id'))
    def remove(self) -> bool:
        """
        Remove workout from db by id.

        :return: True if workout was removed.
        :rtype: bool
        """
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
