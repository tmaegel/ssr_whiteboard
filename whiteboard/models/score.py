# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
import time
import sqlite3
from typing import Any, Union, Optional

from whiteboard.exceptions import (
    ScoreNotFoundError,
    ScoreNoneObjectError,
    ScoreInvalidIdError,
    ScoreInvalidValueError,
    ScoreInvalidRxError,
    ScoreInvalidNoteError,
    ScoreInvalidDatetimeError,
)
from whiteboard.db import get_db
from whiteboard.models.user import User
from whiteboard.models.workout import Workout


class Score():

    def __init__(self, _id: int, _user_id: int, _workout_id: int,
                 _value: str, _rx: bool, _note: str,
                 _datetime: Optional[int] = int(time.time())) -> None:
        self.id = _id
        self.user_id = _user_id
        self.workout_id = _workout_id
        self.value = _value
        self.rx = _rx
        self.note = _note
        self.datetime = _datetime

    def __str__(self):
        return f'Score ( id={self.id},' \
               f' user_id={self.user_id}, workout_id="{self.workout_id}",' \
               f' score={self.score}, rx={self.rx}, datetime={self.datetime} )'

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Score, None]:
        """Create score instance based on the query."""
        if query is None:
            return None

        return Score(
            query['id'],
            query['userId'],
            query['workoutId'],
            query['score'],  # value=score
            True if query['rx'] == 1 else False,
            query['note'],
            query['datetime']
        )

    @staticmethod
    def _validate_object(score: Any) -> None:
        """Simple check if the object is None."""
        if score is None:
            raise ScoreNoneObjectError()

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
        User.get(user_id)

    @staticmethod
    def _validate_workout_id(workout_id: Any) -> None:
        """
        Validate the workout_id by requesting the a workout.
        The validation is done in the workout model.
        """
        Workout.get(workout_id)

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
    def _validate(score: Any) -> None:
        """Check the score object for invalid content."""
        Score._validate_object(score)
        Score._validate_user_id(score.user_id)
        Score._validate_workout_id(score.workout_id)
        Score._validate_value(score.value)
        Score._validate_rx(score.rx)
        Score._validate_note(score.note)
        Score._validate_datetime(score.datetime)

    @staticmethod
    def get(score_id: int) -> Score:
        """Get score from db by id."""
        Score._validate_id(score_id)
        db = get_db()
        result = db.execute(
            'SELECT id, userId, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE id = ?', (score_id,)
        ).fetchone()

        score = Score._query_to_object(result)
        if score is None:
            raise ScoreNotFoundError(score_id=score_id)

        return score

    @staticmethod
    def add(score: Score) -> int:
        """Add new score to db."""
        Score._validate(score)
        db = get_db()
        db.execute(
            'INSERT INTO table_workout_score'
            '(userId, workoutId, score, rx, datetime, note)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (score.user_id, score.workout_id, score.value,
             score.rx, score.datetime, score.note,)
        )
        db.commit()
        inserted_id = db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_workout_score WHERE userId = ? LIMIT 1',
            (score.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    @staticmethod
    def update(score: Score) -> int:
        """Update score in db by id."""
        Score._validate(score)
        Score._validate_id(score.id)
        db = get_db()
        db.execute(
            'UPDATE table_workout_score'
            ' SET workoutId = ?, score = ?, rx = ?, datetime = ?, note = ?'
            ' WHERE id = ? AND userId = ?',
            (score.workout_id, score.value, score.rx, score.datetime,
             score.note, score.id, score.user_id,)
        )
        db.commit()

        return score.id

    @staticmethod
    def remove(score: Score) -> bool:
        """Remove score from db by id."""
        Score._validate_object(score)
        Score._validate_user_id(score.user_id)
        Score._validate_workout_id(score.workout_id)
        Score._validate_id(score.id)
        db = get_db()
        db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE id = ? AND userId = ?', (score.id, score.user_id,)
        )
        db.commit()

        return True
