# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

from typing import Any, Union
from whiteboard.db import get_db
from whiteboard.exceptions import (
    TagInvalidIdError,
    TagInvalidNameError,
    TagNotFoundError,
)
from whiteboard.models.user import User

import json
import logging
import sqlite3

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
    Decorator to validate a tag object.

    :param attr: Attributes of the tag  object to validate.
                 Possible values: id, name
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'name' in attr:
                _validate_tag_name(args[0].name)
            if 'id' in attr:
                _validate_tag_id(args[0].tag_id)
            if 'user_id' in attr:
                _validate_tag_user_id(args[0].user_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_tag_id(tag_id: Any) -> None:
        """Validate the tag id."""
        logger.debug('Validate tag id.')
        if tag_id is None or isinstance(tag_id, bool):
            raise TagInvalidIdError()
        try:
            tag_id = int(tag_id)
        except (ValueError, TypeError):
            raise TagInvalidIdError()
        if tag_id < 0:
            raise TagInvalidIdError()

    def _validate_tag_name(name: Any) -> Any:
        """Validate the tag name."""
        logger.debug('Validate tag name.')
        if name is None or not isinstance(name, str):
            raise TagInvalidNameError()

    def _validate_tag_user_id(user_id: Any) -> None:
        """
        Validate the user_id by requesting the a user.
        The validation is done in the user model.
        """
        logger.debug('Validate tag user id.')
        _user = User(user_id, None, None)
        _user.get()

    return _decorator


class Tag():

    def __init__(self, tag_id: int, user_id: int, name: str) -> None:
        self.tag_id = tag_id
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return f'Tag ( tag_id={self.tag_id}, user_id={self.user_id},' \
               f' name={self.name} )'

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

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

    @validate(attr=('id'))
    def get(self) -> Tag:
        """
        Get tag from db by id.

        :return: Tag object
        :rtype: Tag
        """
        result = self.db.execute(
            'SELECT id, userId, tag FROM table_tags WHERE id = ?',
            (self.tag_id,)
        ).fetchone()

        tag = Tag._query_to_object(result)
        if tag is None:
            raise TagNotFoundError(tag_id=self.tag_id)

        return tag

    @validate(attr=('user_id', 'name'))
    def add(self) -> int:
        """
        Add new tag to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
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

    @validate(attr=('id', 'user_id', 'name'))
    def update(self) -> bool:
        """
        Update tag in db by id.

        :return: True if tag was updated.
        :rtype: bool
        """
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

    @validate(attr=('id', 'user_id'))
    def remove(self) -> bool:
        """
        Remove tag from db by id.

        :return: True if tag was removed.
        :rtype: bool
        """
        # @todo: Remove Connection between tags and tags too
        if not Tag.exist_tag_id(self.tag_id):
            raise TagNotFoundError(tag_id=self.tag_id)

        self.db.execute(
            'DELETE FROM table_tags'
            ' WHERE id = ? AND userId = ?', (self.tag_id, self.user_id,)
        )
        self.db.commit()

        return True
