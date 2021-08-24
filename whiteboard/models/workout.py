# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
import time
from typing import Optional

from whiteboard.db import get_db


class WorkoutNotFoundError(Exception):

    """Custom error that raised when a workout with an id doesn't exist."""

    def __init__(self, workout_id: int) -> None:
        self.workout_id = workout_id
        super().__init__(f'Workout with id {self.workout_id} does not exist.')


class WorkoutNoneObjectError(Exception):

    """Custom error that raised when a workout object is None."""

    def __init__(self) -> None:
        super().__init__('Workout object is None.')


class WorkoutInvalidIdError(Exception):

    """Custom error that raised when a workout contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid workout id.')


class WorkoutInvalidUserIdError(Exception):

    """Custom error that raised when a workout contains a invalid user id."""

    def __init__(self) -> None:
        super().__init__('Invalid user id.')


class WorkoutInvalidNameError(Exception):

    """Custom error that raised when a workout contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid workout name.')


class WorkoutInvalidDescriptionError(Exception):

    """
    Custom error that raised when a workout contains a invalid description.
    """

    def __init__(self) -> None:
        super().__init__('Invalid workout description.')


class WorkoutInvalidTimestampError(Exception):

    """Custom error that raised when a workout contains a invalid timestamp."""

    def __init__(self) -> None:
        super().__init__('Invalid workout timestamp.')


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
    def _query_to_object(query):
        """Create workout instance based on the query."""
        if query is None:
            return None

        return Workout(
            query['id'],
            query['userId'],
            query['name'],
            query['description'],
            query['datetime']
        )

    @staticmethod
    def _validate_object(workout):
        """Simple check if the object is None."""
        if workout is None:
            raise WorkoutNoneObjectError()

    @staticmethod
    def _validate_id(workout_id):
        """Validate the workout id."""
        if workout_id is None:
            raise WorkoutInvalidIdError()
        if (not isinstance(workout_id, int) or
                isinstance(workout_id, bool) or workout_id < 0):
            raise WorkoutInvalidIdError()

    @staticmethod
    def _validate_user_id(user_id):
        """Validate the workout user id."""
        if (user_id is None or
                not isinstance(user_id, int) or
                isinstance(user_id, bool) or user_id < 0):
            raise WorkoutInvalidUserIdError()

    @staticmethod
    def _validate_name(name):
        """Validate the workout name."""
        if name is None or not isinstance(name, str):
            raise WorkoutInvalidNameError()

    @staticmethod
    def _validate_description(description):
        """Validate the workout description."""
        if (description is None or not isinstance(description, str)):
            raise WorkoutInvalidDescriptionError()

    @staticmethod
    def _validate_datetime(datetime):
        """Validate the workout datetime."""
        if (datetime is None or
                not isinstance(datetime, int) or
                isinstance(datetime, bool) or datetime < 0):
            raise WorkoutInvalidTimestampError()

    @staticmethod
    def _validate(workout):
        """Check the workout object for invalid content."""
        # @todo: Check wheather user with user id exist!

        Workout._validate_object(workout)
        Workout._validate_user_id(workout.user_id)
        Workout._validate_name(workout.name)
        Workout._validate_description(workout.description)
        Workout._validate_datetime(workout.datetime)

    @staticmethod
    def get(workout_id: int) -> Workout:
        """Get workout from db by id."""
        Workout._validate_id(workout_id)
        db = get_db()
        result = db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout WHERE id = ?', (workout_id,)
        ).fetchone()

        workout = Workout._query_to_object(result)
        if workout is None:
            raise WorkoutNotFoundError(workout_id=workout_id)

        return workout

    @staticmethod
    def add(workout: Workout) -> int:
        """Add new workout to db."""
        Workout._validate(workout)
        db = get_db()
        db.execute(
            'INSERT INTO table_workout'
            ' (userId, name, description, datetime)'
            ' VALUES (?, ?, ?, ?)',
            (workout.user_id, workout.name, workout.description,
             workout.datetime)
        )
        db.commit()
        inserted_id = db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_workout WHERE userId = ? LIMIT 1',
            (workout.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    @staticmethod
    def update(workout: Workout) -> int:
        """Update workout in db by id."""
        Workout._validate(workout)
        Workout._validate_id(workout.id)
        db = get_db()
        db.execute(
            'UPDATE table_workout'
            ' SET name = ?, description = ?, datetime = ?'
            ' WHERE id = ? AND userId = ?',
            (workout.name, workout.description, int(time.time()),
             workout.id, workout.user_id,)
        )
        db.commit()

        return workout.id

    @staticmethod
    def remove(workout: Workout) -> bool:
        """Remove workout in db by id."""
        Workout._validate_object(workout)
        Workout._validate_user_id(workout.user_id)
        Workout._validate_id(workout.id)
        db = get_db()
        db.execute(
            'DELETE FROM table_workout'
            ' WHERE id = ? AND userId = ?', (workout.id, workout.user_id,)
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
