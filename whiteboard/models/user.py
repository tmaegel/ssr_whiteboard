#!/usr/bin/env python
# coding=utf-8

# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import base64
import hashlib
import json
import sqlite3
from typing import Optional, Union

import bcrypt

from whiteboard import logger
from whiteboard.db import get_db
from whiteboard.decorators import is_defined
from whiteboard.descriptors import Hash, Id, Name
from whiteboard.exceptions import (
    InvalidAttributeError,
    InvalidPasswordError,
    NotFoundError,
)


def is_user_exists(func):
    """
    Decorator to check wheather the user object with id exists.

    :param objects: Objects to be checked for existence.
    """

    def _decorator(*args, **kwargs):
        logger.debug("Check if user exists.")
        try:
            user_id = getattr(args[0], "user_id")
        except AttributeError as exc:
            raise InvalidAttributeError("user_id") from exc
        if not User.exist_user_id(user_id):
            raise NotFoundError(User.__name__, user_id)
        return func(*args, **kwargs)

    return _decorator


class User:

    user_id = Id()
    name = Name()
    password_hash = Hash()

    def __init__(
        self,
        user_id: Optional[int] = None,
        name: Optional[str] = None,
        password_hash: Optional[str] = None,
    ) -> None:
        self.user_id = user_id
        self.name = name
        self.password_hash = password_hash

    def __str__(self):
        return f"User ( user_id={self.user_id}, name={self.name} )"

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @property
    def id(self):
        """The identify handler of flask_jwt expected an id property."""
        return self.user_id

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[User, None]:
        """Create user instance based on the query."""
        if query is None:
            return None

        return User(
            query["id"],  # id=user_id
            query["name"],
            query["password"],  # password=password_hash
        )

    @staticmethod
    def exist_user_id(user_id: int) -> bool:
        """
        Check if user with user id exists by requesting them.

        :param: user id
        :return: True if user with user id exists, otherwise False.
        :rtype: bool
        """
        result = (
            get_db()
            .execute("SELECT id FROM table_users WHERE id = ?", (user_id,))
            .fetchone()
        )

        if result is None:
            return False

        return True

    @is_defined(attributes=("user_id",))
    def get(self) -> User:
        """
        Get user from db by id.

        :return: User object
        :rtype: User
        """
        result = self.db.execute(
            "SELECT id, name, password FROM table_users WHERE id = ?",
            (self.user_id,),
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise NotFoundError(type(self).__name__, self.user_id)

        return user

    @is_defined(attributes=("name",))
    def get_by_name(self) -> User:
        """
        Get user from db by name.

        :return: User object
        :rtype: User
        """
        result = self.db.execute(
            "SELECT id, name, password FROM table_users WHERE name = ?", (self.name,)
        ).fetchone()

        user = User._query_to_object(result)
        if user is None:
            raise NotFoundError(type(self).__name__, self.name)

        return user

    @is_defined(attributes=("name", "password_hash"))
    def add(self) -> int:
        """
        Add new user to db.

        :return: True if user was created.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        self.db.execute(
            "INSERT INTO table_users (name, password) VALUES (?, ?)",
            (self.name, self.password_hash),
        )
        self.db.commit()

        inserted_id = self.db.execute(
            "SELECT last_insert_rowid() FROM table_users LIMIT 1"
        ).fetchone()

        try:
            return int(inserted_id["last_insert_rowid()"])
        except (TypeError, ValueError) as e:
            logger.error("Invalid last_insert_rowid: %s" % e)
            raise

    @is_defined(attributes=("user_id", "name", "password_hash"))
    @is_user_exists
    def update(self) -> bool:
        """
        Update user in db by id.

        :return: True if user was updated.
        :rtype: bool
        """
        # @todo: bcrypt + hash here?
        # gen_password_hash() + check_password() function?
        self.db.execute(
            "UPDATE table_users SET name = ?, password = ? WHERE id = ?",
            (self.name, self.password_hash, self.user_id),
        )
        self.db.commit()

        return True

    @is_defined(attributes=("user_id"))
    @is_user_exists
    def remove(self) -> bool:
        """Remove user from db by id."""
        return True

    @staticmethod
    def authenticate(username: str, password: str) -> Union[User, None]:
        """
        The first being the username the second being the password.
        It should return an user object representing an authenticated
        identity.

        :return: User object
        :rtype: User
        """
        logger.info(f"Authenticate user {username}.")
        user: User = User(None, username, None).get_by_name()

        if user and User.check_password(password, user.password_hash):
            return user

        return None

    @staticmethod
    def check_password(password: str, hash_str: str) -> bool:
        """
        Verify a password against a bcrypt encoded hash.

        :return: True if the password and hash matched. Otherwise false.
        :rtype: boolean
        """
        logger.info("Verifing password.")
        if not password:
            raise InvalidPasswordError()
        pw_byte = password.encode("utf-8")
        pw_hash = base64.b64encode(hashlib.sha256(pw_byte).digest())
        hash_byte = hash_str.encode("utf-8")
        if not bcrypt.checkpw(pw_hash, hash_byte):
            raise InvalidPasswordError()

        return True

    @staticmethod
    def gen_password_hash(password: str) -> str:
        """
        Create a bcrypt encoded hash of a password.

        :return: Hashed password
        :rtype: str
        """
        logger.info("Generating password hash.")
        pw_byte = password.encode("utf-8")
        pw_hash = base64.b64encode(hashlib.sha256(pw_byte).digest())
        hashed = bcrypt.hashpw(pw_hash, bcrypt.gensalt(12))

        return hashed.decode()
