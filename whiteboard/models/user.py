# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import sqlite3
from typing import Any, Union

from whiteboard.db import get_db
from whiteboard.exceptions import (
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
    UserNotFoundError,
)


class User():

    def __init__(self, user_id: int, name: str, password_hash: str) -> None:
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash

        self._db = get_db()

    def __str__(self):
        return f'User ( user_id={self.user_id}, name={self.name} )'

    @property
    def db(self):
        return self._db

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
    def _validate_id(user_id: Any) -> None:
        """Validate the user id."""
        if (user_id is None or not isinstance(user_id, int) or
                isinstance(user_id, bool) or user_id < 0):
            raise UserInvalidIdError()

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the user name."""
        # @todo: Allow only [a-zA-Z0-9]
        if name is None or not isinstance(name, str):
            raise UserInvalidNameError()

    @staticmethod
    def _validate_password_hash(password_hash: Any) -> None:
        """Validate the user password_hash."""
        if password_hash is None or not isinstance(password_hash, str):
            raise UserInvalidPasswordError()

    def get(self) -> User:
        """
        Get user from db by id.

        :return: User object
        :rtype: User
        """
        User._validate_id(self.user_id)
        result = self.db.execute(
            'SELECT id, name, password FROM table_users'
            ' WHERE id = ?', (self.user_id,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=self.user_id)

        return user

    def get_by_name(self) -> User:
        """
        Get user from db by name.

        :return: User object
        :rtype: User
        """
        User._validate_name(self.name)
        result = self.db.execute(
            'SELECT id, name, password FROM table_users'
            ' WHERE name = ?', (self.name,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=self.name)

        return user

    def add(self) -> bool:
        """
        Add new user to db.

        :return: True if user was created.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        User._validate_name(self.name)
        User._validate_password_hash(self.password_hash)
        self.db.execute(
            'INSERT INTO table_users'
            ' (name, password)'
            ' VALUES (?, ?)', (self.name, self.password_hash)
        )
        self.db.commit()

        return True

    def update(self) -> bool:
        """
        Update user in db by id.

        :return: True if user was updated.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        User._validate_id(self.user_id)
        User._validate_name(self.name)
        User._validate_password_hash(self.password_hash)
        self.db.execute(
            'UPDATE table_users'
            ' SET name = ?, password = ?'
            ' WHERE id = ?',
            (self.name, self.password_hash, self.user_id)
        )
        self.db.commit()

        return True

    def Remove(self) -> bool:
        """Remove user from db by id."""
        pass
