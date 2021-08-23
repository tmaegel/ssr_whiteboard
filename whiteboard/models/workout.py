# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
import time
from typing import Optional, Union

from ..db import get_db


class WorkoutNotFoundError(Exception):

    """Custom error that raised when a workout with an id doesn't exist."""

    def __init__(self, _message: str) -> None:
        self.message = _message
        super().__init__(_message)


class WorkoutNoneObjectError(Exception):

    """Custom error that raised when a workout object is None."""

    def __init__(self, _message: str) -> None:
        self.message = _message
        super().__init__(_message)


class WorkoutInvalidIdError(Exception):

    """Custom error that raised when a workout contains a invalid id."""

    def __init__(self, _message: str) -> None:
        self.message = _message


class WorkoutInvalidUserIdError(Exception):

    """Custom error that raised when a workout contains a invalid user id."""

    def __init__(self, _message: str) -> None:
        self.message = _message
        super().__init__(_message)


class WorkoutInvalidNameError(Exception):

    """Custom error that raised when a workout contains a invalid name."""

    def __init__(self, _message: str) -> None:
        self.message = _message


class WorkoutInvalidDescriptionError(Exception):

    """
    Custom error that raised when a workout contains a invalid description.
    """

    def __init__(self, _message: str) -> None:
        self.message = _message


class WorkoutInvalidTimestampError(Exception):

    """Custom error that raised when a workout contains a invalid timestamp."""

    def __init__(self, _message: str) -> None:
        self.message = _message


class Workout():

    def __init__(self, _id: int, _user_id: int, _name: str, _description: str,
                 _datetime: Optional[int] = int(time.time())) -> None:
        self.id = _id
        self.user_id = _user_id
        self.name = _name
        self.description = _description
        self.datetime = _datetime

    def __str__(self):
        return f'Workout ( identifier={self.identifier},' \
               f' user_id={self.user_id}, name="{self.name}",' \
               f' datetime={self.datetime} )'

    @staticmethod
    def _query_to_object(_query):
        """Create workout instance based on the query."""
        if _query is None:
            return None

        return Workout(
            _query['id'],
            _query['userId'],
            _query['name'],
            _query['description'],
            _query['datetime']
        )

    @staticmethod
    def _validate_object(_workout):
        """Simple check if the object is None."""
        if _workout is None:
            raise WorkoutNoneObjectError('Workout object is None.')

    @staticmethod
    def _validate_id(_id):
        """Validate the workout id."""
        if _id is None:
            raise WorkoutInvalidIdError('Given workout id is "None".')
        if (not isinstance(_id, int) or
                isinstance(_id, bool) or _id < 0):
            raise WorkoutInvalidIdError('Invalid workout id.')

    @staticmethod
    def _validate_user_id(_user_id):
        """Validate the workout user id."""
        if (_user_id is None or
                not isinstance(_user_id, int) or
                isinstance(_user_id, bool) or _user_id < 0):
            raise WorkoutInvalidUserIdError('Workout has invalid user id.')

    @staticmethod
    def _validate_name(_name):
        """Validate the workout name."""
        if _name is None or not isinstance(_name, str):
            raise WorkoutInvalidNameError('Workout has invalid name.')

    @staticmethod
    def _validate_description(_description):
        """Validate the workout description."""
        if (_description is None or not isinstance(_description, str)):
            raise WorkoutInvalidDescriptionError(
                'Workout has invalid description.')

    @staticmethod
    def _validate_datetime(_datetime):
        """Validate the workout datetime."""
        if (_datetime is None or
                not isinstance(_datetime, int) or
                isinstance(_datetime, bool) or _datetime < 0):
            raise WorkoutInvalidTimestampError(
                'Workout has invalid timestamp.')

    @staticmethod
    def _validate(_workout):
        """Check the workout object for invalid content."""
        # @todo: Check wheather user with user id exist!

        Workout._validate_object(_workout)
        Workout._validate_user_id(_workout.user_id)
        Workout._validate_name(_workout.name)
        Workout._validate_description(_workout.description)
        Workout._validate_datetime(_workout.datetime)

    @staticmethod
    def get(_id: int) -> Workout:
        """Get workout from db by id."""
        Workout._validate_id(_id)
        db = get_db()
        result = db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout WHERE id = ?', (_id,)
        ).fetchone()

        workout = Workout._query_to_object(result)
        if workout is None:
            raise WorkoutNotFoundError(
                'Workout ' + str(_id) + ' does not exist.'
            )

        return workout

    @staticmethod
    def add(_workout: Workout) -> int:
        """Add new workout to db."""
        Workout._validate(_workout)
        db = get_db()
        db.execute(
            'INSERT INTO table_workout'
            ' (userId, name, description, datetime)'
            ' VALUES (?, ?, ?, ?)',
            (_workout.user_id, _workout.name, _workout.description,
             _workout.datetime)
        )
        db.commit()
        inserted_id = db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_workout WHERE userId = ? LIMIT 1',
            (_workout.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    @staticmethod
    def update(_workout: Workout) -> int:
        """Update workout in db by id."""
        Workout._validate(_workout)
        Workout._validate_id(_workout.id)
        db = get_db()
        db.execute(
            'UPDATE table_workout'
            ' SET name = ?, description = ?, datetime = ?'
            ' WHERE id = ? AND userId = ?',
            (_workout.name, _workout.description, int(time.time()),
             _workout.id, _workout.user_id,)
        )
        db.commit()

        return _workout.id

    @staticmethod
    def remove(_workout: Workout) -> bool:
        """Remove workout in db by id."""
        Workout._validate_object(_workout)
        Workout._validate_user_id(_workout.user_id)
        Workout._validate_id(_workout.id)
        db = get_db()
        db.execute(
            'DELETE FROM table_workout'
            ' WHERE id = ? AND userId = ?', (_workout.id, _workout.user_id,)
        )
        db.commit()
        # @todo: use current delete_score function
        # db.execute(
        #     'DELETE FROM table_workout_score'
        #     ' WHERE workoutId = ? AND userId = ?',
        #     (workout_id, g.user['id'],)
        # )
        # db.commit()

        return True
