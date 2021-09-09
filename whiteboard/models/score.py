# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
import time
from typing import Any, Optional, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    ScoreInvalidDatetimeError,
    ScoreInvalidIdError,
    ScoreInvalidNoteError,
    ScoreInvalidRxError,
    ScoreInvalidValueError,
    ScoreNotFoundError,
)
from whiteboard.models.user import User
from whiteboard.models.workout import Workout


class Score():

    def __init__(self, score_id: int, user_id: int, workout_id: int,
                 value: str, rx: bool, note: str,
                 datetime: Optional[int] = int(time.time())) -> None:
        self.score_id = score_id
        self.user_id = user_id
        self.workout_id = workout_id
        self.value = value
        self.rx = rx
        self.note = note
        self.datetime = datetime

        self._db = get_db()

    def __str__(self):
        return f'Score ( score_id={self.score_id},' \
               f' user_id={self.user_id}, workout_id="{self.workout_id}",' \
               f' score={self.score}, rx={self.rx}, datetime={self.datetime} )'

    @property
    def db(self):
        return self._db

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Score, None]:
        """Create score instance based on the query."""
        if query is None:
            return None

        return Score(
            query['id'],  # id=score_id
            query['userId'],
            query['workoutId'],
            query['score'],  # value=score
            True if query['rx'] == 1 else False,
            query['note'],
            query['datetime']
        )

    @staticmethod
    def _validate_id(score_id: Any) -> None:
        """Validate the score id."""
        if (score_id is None or not isinstance(score_id, int) or
                isinstance(score_id, bool) or score_id < 0):
            raise ScoreInvalidIdError()

    @staticmethod
    def _validate_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        _user = User(user_id, None, None)
        _user.get()

    @staticmethod
    def _validate_workout_id(workout_id: Any) -> None:
        """
        Validate the workout_id by requesting the a workout.
        The validation is done in the workout model.
        """
        _workout = Workout(workout_id, None, None, None)
        _workout.get()

    @staticmethod
    def _validate_value(value: Any) -> None:
        """Validate the score value."""
        if value is None or not isinstance(value, str):
            raise ScoreInvalidValueError()

    @staticmethod
    def _validate_rx(rx: Any) -> None:
        """Validate the score rx state."""
        if (rx is None or not isinstance(rx, bool)):
            raise ScoreInvalidRxError()

    @staticmethod
    def _validate_note(note: Any) -> None:
        """Validate the note description."""
        if (note is None or not isinstance(note, str)):
            raise ScoreInvalidNoteError()

    @staticmethod
    def _validate_datetime(datetime: Any) -> None:
        """Validate the score datetime."""
        if (datetime is None or
                not isinstance(datetime, int) or
                isinstance(datetime, bool) or datetime < 0):
            raise ScoreInvalidDatetimeError()

    @staticmethod
    def exist_score_id(score_id: int) -> bool:
        """
        Check if score with score id exists by requesting them.

        :param: score id
        :return: True if score with score id exists, otherwise False.
        :rtype: bool
        """
        result = get_db().execute(
            'SELECT id, userId, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE id = ?', (score_id,)
        ).fetchone()

        if result is None:
            return False
        else:
            return True

    def get(self) -> Score:
        """
        Get score from db by id.

        :return: Score object
        :rtype: Score
        """
        Score._validate_id(self.score_id)
        result = self.db.execute(
            'SELECT id, userId, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE id = ?', (self.score_id,)
        ).fetchone()

        score = Score._query_to_object(result)
        if score is None:
            raise ScoreNotFoundError(score_id=self.score_id)

        return score

    def add(self) -> int:
        """
        Add new score to db.

        :return: Return the id of the created score.
        :rtype: int
        """
        Score._validate_value(self.value)
        Score._validate_rx(self.rx)
        Score._validate_note(self.note)
        Score._validate_datetime(self.datetime)
        Score._validate_workout_id(self.workout_id)
        Score._validate_user_id(self.user_id)
        self.db.execute(
            'INSERT INTO table_workout_score'
            '(userId, workoutId, score, rx, datetime, note)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (self.user_id, self.workout_id, self.value,
             self.rx, self.datetime, self.note,)
        )
        self.db.commit()
        inserted_id = self.db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_workout_score WHERE userId = ? LIMIT 1',
            (self.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    def update(self) -> bool:
        """
        Update score in db by id.

        :return: True if score was updated.
        :rtype: bool
        """
        Score._validate_value(self.value)
        Score._validate_rx(self.rx)
        Score._validate_note(self.note)
        Score._validate_datetime(self.datetime)
        Score._validate_workout_id(self.workout_id)
        Score._validate_user_id(self.user_id)
        Score._validate_id(self.score_id)

        if not Score.exist_score_id(self.score_id):
            raise ScoreNotFoundError(score_id=self.score_id)

        self.db.execute(
            'UPDATE table_workout_score'
            ' SET workoutId = ?, score = ?, rx = ?, datetime = ?, note = ?'
            ' WHERE id = ? AND userId = ?',
            (self.workout_id, self.value, self.rx, self.datetime,
             self.note, self.score_id, self.user_id,)
        )
        self.db.commit()

        return True

    def remove(self) -> bool:
        """
        Remove score from db by id.

        :return: True if score was removed.
        :rtype: bool
        """
        Score._validate_workout_id(self.workout_id)
        Score._validate_user_id(self.user_id)
        Score._validate_id(self.score_id)

        if not Score.exist_score_id(self.score_id):
            raise ScoreNotFoundError(score_id=self.score_id)

        self.db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE id = ? AND userId = ?', (self.score_id, self.user_id,)
        )
        self.db.commit()

        return True
