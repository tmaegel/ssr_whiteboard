# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
from typing import Any, Union
import sqlite3

from whiteboard.db import get_db


class UserNotFoundError(Exception):

    """Custom error that raised when a user with an id doesn't exist."""

    def __init__(self, identifier: Union[int, str]) -> None:
        self.identifier = identifier
        super().__init__(
            f'User with id or name {self.identifier} does not exist.')


class UserInvalidIdError(Exception):

    """Custom error that raised when a user contains a invalid id."""

    def __init__(self) -> None:
        super().__init__('Invalid user id.')


class UserInvalidNameError(Exception):

    """Custom error that raised when a user contains a invalid name."""

    def __init__(self) -> None:
        super().__init__('Invalid user name.')


class User():

    def __init__(self, _id: int, _name: str, _password: str) -> None:
        self.id = _id
        self.name = _name
        self.password = _password

    def __str__(self):
        return f'User ( id={self.id}, name={self.name} )'

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[User, None]:
        """Create user instance based on the query."""
        if query is None:
            return None

        return User(
            query['id'],
            query['name'],
            query['password'],
        )

    @staticmethod
    def _validate_id(user_id: Any) -> None:
        """Validate the user id."""
        if user_id is None:
            raise UserInvalidIdError()
        if (not isinstance(user_id, int) or
                isinstance(user_id, bool) or user_id < 0):
            raise UserInvalidIdError()

    @staticmethod
    def _validate_name(name: Any) -> None:
        """Validate the user name."""
        if name is None or not isinstance(name, str):
            raise UserInvalidNameError()

    @staticmethod
    def get(user_id: int) -> User:
        """Get user from db by id."""
        User._validate_id(user_id)
        db = get_db()
        result = db.execute(
            'SELECT id, name, password FROM table_users WHERE id = ?',
            (user_id,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=user_id)

        return user

    @staticmethod
    def get_by_name(name: str) -> User:
        """Get user from db by name."""
        User._validate_name(name)
        db = get_db()
        result = db.execute(
            'SELECT id, name, password FROM table_users WHERE name = ?',
            (name,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise UserNotFoundError(identifier=name)

        return user

    @staticmethod
    def add(user: User) -> int:
        """Add new user to db."""
        pass

    @staticmethod
    def update(user: User) -> int:
        """Update user in db by id."""
        pass

    @staticmethod
    def Remove(user: User) -> int:
        """Remove user from db by id."""
        pass
