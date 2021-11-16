# -*- coding: utf-8 -*-
# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

from typing import Optional, Union
from whiteboard.db import get_db
from whiteboard.decorators import is_defined
from whiteboard.descriptors import Bool, Id, Name, Text, UnixTimestamp
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import is_user_exists
from whiteboard.models.workout import is_workout_exists

import json
import sqlite3
import time
import whiteboard.logger as logger


def is_score_exists(func):
    """
    Decorator to check wheather the score object with id exists.

    :param objects: Objects to be checked for existence.
    """
    def _decorator(*args, **kwargs):
        logger.debug('Check if score exists.')
        try:
            score_id = getattr(args[0], 'score_id')
        except AttributeError:
            raise InvalidAttributeError('score_id')
        if not Score.exist_score_id(score_id):
            raise NotFoundError(Score.__name__, score_id)
        return func(*args, **kwargs)
    return _decorator


def is_owner(func):
    """
    Decorator to check wheather the score is owned by user.
    """
    def _decorator(*args, **kwargs):
        # @todo
        return func(*args, **kwargs)
    return _decorator


class Score():

    score_id = Id()
    user_id = Id()
    workout_id = Id()
    value = Name()  # @todo: ScoreValue: valid values: HH:MM:SS and int/float
    rx = Bool()  # @todo: valid values: true/false, TRUE/FALSE, 1/0 -> format!
    note = Text()
    datetime = UnixTimestamp()

    def __init__(self,
                 score_id: int = None,
                 user_id: int = None,
                 workout_id: int = None,
                 value: str = None,
                 rx: bool = None,
                 note: str = None,
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

    @property
    def id(self):
        return self.score_id

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
            'SELECT id FROM table_workout_score WHERE id = ?',
            (score_id,)
        ).fetchone()

        if result is None:
            return False
        else:
            return True

    @is_defined(attributes=('score_id', 'user_id'))
    @is_user_exists
    def get(self) -> Score:
        """
        Get score from db by id.

        :return: Score object
        :rtype: Score
        """
        result = self.db.execute(
            'SELECT id, userId, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE id = ? and userId = ?',
            (self.score_id, self.user_id)
        ).fetchone()

        score = Score._query_to_object(result)
        if score is None:
            raise NotFoundError(type(self).__name__, self.score_id)

        return score

    @is_defined(attributes=('user_id', 'workout_id', 'value', 'rx', 'note',
                            'datetime'))
    @is_workout_exists
    @is_user_exists
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
            ' FROM table_workout_score'
            ' WHERE userId = ? and workoutId = ? LIMIT 1',
            (self.user_id, self.workout_id)
        ).fetchone()

        try:
            return int(inserted_id['last_insert_rowid()'])
        except (TypeError, ValueError) as e:
            logger.error('Invalid last_insert_rowid: %s' % str(e))
            raise

    @is_defined(attributes=('score_id', 'user_id', 'workout_id', 'value', 'rx',
                            'note', 'datetime'))
    @is_score_exists
    @is_workout_exists
    @is_user_exists
    def update(self) -> bool:
        """
        Update score in db by id.

        :return: True if score was updated.
        :rtype: bool
        """
        self.db.execute(
            'UPDATE table_workout_score'
            ' SET workoutId = ?, score = ?, rx = ?, datetime = ?, note = ?'
            ' WHERE id = ? AND userId = ? AND workoutId = ?',
            (self.workout_id, self.value, self.rx, self.datetime,
             self.note, self.score_id, self.user_id, self.workout_id)
        )
        self.db.commit()

        return True

    @is_defined(attributes=('score_id', 'user_id', 'workout_id'))
    @is_score_exists
    @is_workout_exists
    @is_user_exists
    def remove(self) -> bool:
        """
        Remove score from db by id.

        :return: True if score was removed.
        :rtype: bool
        """
        self.db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE id = ? AND userId = ? AND workoutId = ?',
            (self.score_id, self.user_id, self.workout_id)
        )
        self.db.commit()

        return True
