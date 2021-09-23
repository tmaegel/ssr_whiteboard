# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

from typing import Any, Union
from whiteboard.db import get_db
from whiteboard.exceptions import (
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
    UserNotFoundError,
)

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
    Decorator to validate a user object.

    :param attr: Attributes of the workout object to validate.
                 Possible values: id, name, password_hash
    """

    def _decorator(func):
        def _wrapper(*args, **kwargs):
            logger.debug('Call function %r with attributes %r.' % (func, attr))
            logger.debug('Validate object %s' % args[0])
            if 'name' in attr:
                _validate_user_name(args[0].name)
            if 'password_hash' in attr:
                _validate_user_password_hash(args[0].password_hash)
            if 'id' in attr:
                _validate_user_id(args[0].user_id)
            return func(*args, **kwargs)
        return _wrapper

    def _validate_user_id(user_id: Any) -> None:
        """Validate the user id."""
        logger.debug('Validate user id.')
        if user_id is None or isinstance(user_id, bool):
            raise UserInvalidIdError()
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise UserInvalidIdError()
        if user_id < 0:
            raise UserInvalidIdError()

    def _validate_user_name(name: Any) -> Any:
        """Validate the user name."""
        logger.debug('Validate user name.')
        if name is None or not isinstance(name, str):
            raise UserInvalidNameError()

    def _validate_user_password_hash(password_hash: Any) -> None:
        """Validate the user password_hash."""
        if password_hash is None or not isinstance(password_hash, str):
            raise UserInvalidPasswordError()

    return _decorator


class User():

    def __init__(self, user_id: int, name: str, password_hash: str) -> None:
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash

    def __str__(self):
        return f'User ( user_id={self.user_id}, name={self.name} )'

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[User, None]:
        """Create user instance based on the query."""
        if query is None:
            return None

        return User(
            query['id'],  # id=user_id
            query['name'],
            query['password'],  # password=password_hash
        )

    @staticmethod
    def exist_user_id(user_id: int) -> bool:
        """
        Check if user with user id exists by requesting them.

        :param: user id
        :return: True if user with user id exists, otherwise False.
        :rtype: bool
        """
        result = get_db().execute(
            'SELECT id, name, password FROM table_users'
            ' WHERE id = ?', (user_id,)
        ).fetchone()

        if result is None:
            return False
        else:
            return True

    @validate(attr=('id'))
    def get(self) -> User:
        """
        Get user from db by id.

        :return: User object
        :rtype: User
        """
        result = self.db.execute(
            'SELECT id, name, password FROM table_users'
            ' WHERE id = ?', (self.user_id,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=self.user_id)

        return user

    @validate(attr=('name'))
    def get_by_name(self) -> User:
        """
        Get user from db by name.

        :return: User object
        :rtype: User
        """
        result = self.db.execute(
            'SELECT id, name, password FROM table_users'
            ' WHERE name = ?', (self.name,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=self.name)

        return user

    @validate(attr=('name', 'password_hash'))
    def add(self) -> bool:
        """
        Add new user to db.

        :return: True if user was created.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        self.db.execute(
            'INSERT INTO table_users'
            ' (name, password)'
            ' VALUES (?, ?)', (self.name, self.password_hash)
        )
        self.db.commit()

        return True

    @validate(attr=('id', 'name', 'password_hash'))
    def update(self) -> bool:
        """
        Update user in db by id.

        :return: True if user was updated.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        if not User.exist_user_id(self.user_id):
            raise UserNotFoundError(identifier=self.user_id)

        self.db.execute(
            'UPDATE table_users'
            ' SET name = ?, password = ?'
            ' WHERE id = ?',
            (self.name, self.password_hash, self.user_id)
        )
        self.db.commit()

        return True

    @validate(attr=('id'))
    def Remove(self) -> bool:
        """Remove user from db by id."""
        pass
