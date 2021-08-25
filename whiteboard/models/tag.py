# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
from typing import Any, Union
import sqlite3

from whiteboard.exceptions import (
    TagNotFoundError,
    TagNoneObjectError,
    TagInvalidIdError,
    TagInvalidNameError,
)
from whiteboard.db import get_db
from whiteboard.models.user import User


class Tag():

    def __init__(self, _id: int, _user_id: int, _name: str) -> None:
        self.id = _id
        self.user_id = _user_id
        self.name = _name

    def __str__(self):
        return f'Tag ( id={self.id}, user_id={self.user_id},' \
               f' name={self.name} )'

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Tag, None]:
        """Create tag instance based on the query."""
        if query is None:
            return None

        return Tag(
            query['id'],
            query['userId'],
            query['tag'],  # name=tag
        )

    @staticmethod
    def _validate_object(tag: Any) -> None:
        """Simple check if the object is None."""
        if tag is None:
            raise TagNoneObjectError()

    @staticmethod
    def _validate_id(tag_id: Any) -> None:
        """Validate the tag id."""
        if (tag_id is None or not isinstance(tag_id, int) or
                isinstance(tag_id, bool) or tag_id < 0):
            raise TagInvalidIdError()

    @staticmethod
    def _validate_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        User.get(user_id)

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the tag name."""
        if name is None or not isinstance(name, str):
            raise TagInvalidNameError()

    @staticmethod
    def _validate(tag: Any) -> None:
        """Check the tag object for invalid content."""
        Tag._validate_object(tag)
        Tag._validate_user_id(tag.user_id)
        Tag._validate_name(tag.name)

    @staticmethod
    def get(tag_id: int) -> Tag:
        """Get tag from db by id."""
        Tag._validate_id(tag_id)
        db = get_db()
        result = db.execute(
            'SELECT id, userId, tag FROM table_tags WHERE id = ?',
            (tag_id,)
        ).fetchone()

        tag = Tag._query_to_object(result)
        if tag is None:
            raise TagNotFoundError(tag_id=tag_id)

        return tag

    @staticmethod
    def add(tag: Tag) -> int:
        """Add new tag to db."""
        Tag._validate(tag)
        db = get_db()
        db.execute(
            'INSERT INTO table_tags'
            ' (userId, tag)' ' VALUES (?, ?)', (tag.user_id, tag.name,)
        )
        db.commit()
        inserted_id = db.execute(
            'SELECT last_insert_rowid()'
            ' FROM table_tags WHERE userId = ? LIMIT 1',
            (tag.user_id,)
        ).fetchone()

        return inserted_id['last_insert_rowid()']

    @staticmethod
    def update(tag: Tag) -> int:
        """Update tag in db by id."""
        Tag._validate(tag)
        Tag._validate_id(tag.id)
        db = get_db()
        db.execute(
            'UPDATE table_tags'
            ' SET tag = ?'
            ' WHERE id = ? AND userId = ?',
            (tag.name, tag.id, tag.user_id,)
        )
        db.commit()

        return tag.id

    @staticmethod
    def remove(tag: Tag) -> bool:
        """Remove tag from db by id."""
        Tag._validate_object(tag)
        Tag._validate_user_id(tag.user_id)
        Tag._validate_id(tag.id)
        db = get_db()
        db.execute(
            'DELETE FROM table_tags'
            ' WHERE id = ? AND userId = ?', (tag.id, tag.user_id,)
        )
        db.commit()
        # @todo
        # Remove Connection between tags and workouts

        return True
