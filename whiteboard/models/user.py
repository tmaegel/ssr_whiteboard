# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations
from typing import Any, Union
import sqlite3

from whiteboard.exceptions import (
    UserNotFoundError,
    UserNoneObjectError,
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
)
from whiteboard.db import get_db


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
    def _validate_object(user: Any) -> None:
        """Simple check if the object is None."""
        if user is None:
            raise UserNoneObjectError()

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
    def _validate_password(password: Any) -> None:
        """Validate the user password."""
        # @todo: Force minimal length of the password
        if password is None or not isinstance(password, str):
            raise UserInvalidPasswordError()

    @staticmethod
    def _validate(user: Any) -> None:
        """Check the user object for invalid content."""
        User._validate_object(user)
        User._validate_name(user.name)
        User._validate_password(user.password)

    @staticmethod
    def get(user_id: int) -> User:
        """
        Get user from db by id.

        :param name: Id of user
        :return: User object
        :rtype: User
        """
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
        """
        Get user from db by name.

        :param name: Name of user
        :return: User object
        :rtype: User
        """
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
    def add(user: User) -> str:
        """
        Add new user to db.

        :param user: User object
        :return: Name of created user
        :rtype: str
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        User._validate(user)
        db = get_db()
        db.execute(
            'INSERT INTO table_users'
            ' (name, password)'
            ' VALUES (?, ?)', (user.name, user.password)
        )
        db.commit()

        return user.name

    @staticmethod
    def update(user: User) -> int:
        """
        Update user in db by id.

        :param user: User object
        :return: Id of updated user
        :rtype: int
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        User._validate(user)
        User._validate_id(user.id)
        db = get_db()
        db.execute(
            'UPDATE table_users'
            ' SET name = ?, password = ?'
            ' WHERE id = ?',
            (user.name, user.password, user.id)
        )
        db.commit()

        return user.id

    @staticmethod
    def Remove(user: User) -> int:
        """Remove user from db by id."""
        pass
