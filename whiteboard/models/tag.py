# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
from typing import Any, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    TagInvalidIdError,
    TagInvalidNameError,
    TagNotFoundError,
)
from whiteboard.models.user import User


class Tag():

    def __init__(self, tag_id: int, user_id: int, name: str) -> None:
        self.tag_id = tag_id
        self.user_id = user_id
        self.name = name

        self._db = get_db()

    def __str__(self):
        return f'Tag ( tag_id={self.tag_id}, user_id={self.user_id},' \
               f' name={self.name} )'

    @property
    def db(self):
        return self._db

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Tag, None]:
        """Create tag instance based on the query."""
        if query is None:
            return None

        return Tag(
            query['id'],  # id=tag_id
            query['userId'],
            query['tag'],  # name=tag
        )

    @staticmethod
    def _validate_id(tag_id: Any) -> None:
        """Validate the tag id."""
        # @todo: Check if tag exists by reqeuesting it.
        if (tag_id is None or not isinstance(tag_id, int) or
                isinstance(tag_id, bool) or tag_id < 0):
            raise TagInvalidIdError()

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
        """Validate the tag name."""
        if name is None or not isinstance(name, str):
            raise TagInvalidNameError()

    @staticmethod
    def exist_tag_id(tag_id: int) -> bool:
        """
        Check if tag with tag id exists by requesting them.

        :param: tag id
        :return: True if tag with tag id exists, otherwise False.
        :rtype: bool
        """
        result = get_db().execute(
            'SELECT id, userId, tag FROM table_tags WHERE id = ?',
            (tag_id,)
        ).fetchone()

        if result is None:
            return False
        else:
            return True

    def get(self) -> Tag:
        """
        Get tag from db by id.

        :return: Tag object
        :rtype: Tag
        """
        Tag._validate_id(self.tag_id)
        result = self.db.execute(
            'SELECT id, userId, tag FROM table_tags WHERE id = ?',
            (self.tag_id,)
        ).fetchone()

        tag = Tag._query_to_object(result)
        if tag is None:
            raise TagNotFoundError(tag_id=self.tag_id)

        return tag

    def add(self) -> int:
        """
        Add new tag to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
        Tag._validate_name(self.name)
        Tag._validate_user_id(self.user_id)
        self.db.execute(
            'INSERT INTO table_tags'
            ' (userId, tag)' ' VALUES (?, ?)', (self.user_id, self.name,)
        )
        self.db.commit()
        inserted_id = self.db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_tags WHERE userId = ? LIMIT 1',
            (self.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    def update(self) -> bool:
        """
        Update tag in db by id.

        :return: True if tag was updated.
        :rtype: bool
        """
        Tag._validate_id(self.tag_id)
        Tag._validate_name(self.name)
        Tag._validate_user_id(self.user_id)

        if not Tag.exist_tag_id(self.tag_id):
            raise TagNotFoundError(tag_id=self.tag_id)

        self.db.execute(
            'UPDATE table_tags'
            ' SET tag = ?'
            ' WHERE id = ? AND userId = ?',
            (self.name, self.tag_id, self.user_id,)
        )
        self.db.commit()

        return True

    def remove(self) -> bool:
        """
        Remove tag from db by id.

        :return: True if tag was removed.
        :rtype: bool
        """
        # @todo: Remove Connection between tags and workouts too
        Tag._validate_id(self.tag_id)
        Tag._validate_user_id(self.user_id)

        if not Tag.exist_tag_id(self.tag_id):
            raise TagNotFoundError(tag_id=self.tag_id)

        self.db.execute(
            'DELETE FROM table_tags'
            ' WHERE id = ? AND userId = ?', (self.tag_id, self.user_id,)
        )
        self.db.commit()

        return True
