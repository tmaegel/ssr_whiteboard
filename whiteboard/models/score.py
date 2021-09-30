# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

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
    Decorator to validate a score object.

    :param attr: Attributes of the scpre object to validate.
                 Possible values: id, user_id, workout_id, value, rx, note,
                                  datetime
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'value' in attr:
                _validate_score_value(args[0].value)
            if 'rx' in attr:
                _validate_score_rx(args[0].rx)
            if 'note' in attr:
                _validate_score_note(args[0].note)
            if 'datetime' in attr:
                _validate_score_datetime(args[0].datetime)
            if 'id' in attr:
                _validate_score_id(args[0].score_id)
            if 'user_id' in attr:
                _validate_score_user_id(args[0].user_id)
            if 'workout_id' in attr:
                _validate_score_workout_id(args[0].workout_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_score_id(score_id: Any) -> None:
        """Validate the score id."""
        logger.debug('Validate score id.')
        if score_id is None or isinstance(score_id, bool):
            logger.error('Invalid score id.')
            raise ScoreInvalidIdError()
        try:
            score_id = int(score_id)
        except (ValueError, TypeError):
            logger.error('Invalid score id.')
            raise ScoreInvalidIdError()
        if score_id < 0:
            logger.error('Invalid score id.')
            raise ScoreInvalidIdError()

    def _validate_score_value(value: Any) -> Any:
        """Validate the score value."""
        logger.debug('Validate score value.')
        if value is None or not isinstance(value, str):
            logger.error('Invalid score value.')
            raise ScoreInvalidValueError()

    def _validate_score_rx(rx: Any) -> Any:
        """Validate the score rx state."""
        logger.debug('Validate score rx state.')
        if (rx is None or not isinstance(rx, bool)):
            logger.error('Invalid score rx state.')
            raise ScoreInvalidRxError()

    def _validate_score_note(note: Any) -> None:
        """Validate the score note."""
        logger.debug('Validate score note.')
        if (note is None or not isinstance(note, str)):
            logger.error('Invalid score note.')
            raise ScoreInvalidNoteError()

    def _validate_score_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        logger.debug('Validate score user id.')
        _user = User(user_id, None, None)
        _user.get()

    def _validate_score_workout_id(workout_id: Any) -> None:
        """
        Validate the workout_id by requesting the a workout.
        The validation is done in the workout model.
        """
        logger.debug('Validate score workout id.')
        _workout = Workout(workout_id, None, None, None)
        _workout.get()

    def _validate_score_datetime(datetime: Any) -> None:
        """Validate the score datetime."""
        logger.debug('Validate score datetime.')
        if (datetime is None or isinstance(datetime, bool) or
                isinstance(datetime, float)):
            logger.error('Invalid score datetime.')
            raise ScoreInvalidDatetimeError()
        try:
            datetime = int(datetime)
        except (ValueError, TypeError):
            logger.error('Invalid score datetime.')
            raise ScoreInvalidDatetimeError()
        if datetime < 0:
            logger.error('Invalid score datetime.')
            raise ScoreInvalidDatetimeError()

    return _decorator


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

    def __str__(self):
        return f'Score ( score_id={self.score_id},' \
               f' user_id={self.user_id}, workout_id="{self.workout_id}",' \
               f' score={self.value}, rx={self.rx}, datetime={self.datetime} )'

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

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

    @validate(attr=('id'))
    def get(self) -> Score:
        """
        Get score from db by id.

        :return: Score object
        :rtype: Score
        """
        result = self.db.execute(
            'SELECT id, userId, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE id = ?', (self.score_id,)
        ).fetchone()

        score = Score._query_to_object(result)
        if score is None:
            raise ScoreNotFoundError(score_id=self.score_id)

        return score

    @validate(attr=('user_id', 'workout_id', 'value', 'rx', 'note', 'datetime'))
    def add(self) -> int:
        """
        Add new score to db.

        :return: Return the id of the created score.
        :rtype: int
        """
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

    @validate(attr=('id', 'user_id', 'workout_id', 'value', 'rx', 'note', 'datetime'))
    def update(self) -> bool:
        """
        Update score in db by id.

        :return: True if score was updated.
        :rtype: bool
        """
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

    @validate(attr=('id', 'user_id', 'workout_id'))
    def remove(self) -> bool:
        """
        Remove score from db by id.

        :return: True if score was removed.
        :rtype: bool
        """
        if not Score.exist_score_id(self.score_id):
            raise ScoreNotFoundError(score_id=self.score_id)

        self.db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE id = ? AND userId = ?', (self.score_id, self.user_id,)
        )
        self.db.commit()

        return True
