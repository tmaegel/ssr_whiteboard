#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PEP 563: Postponed Evaluation of Annotations
# It will become the default in Python 3.10.
from __future__ import annotations

import json
import sqlite3
from typing import Optional, Union

from whiteboard import logger
from whiteboard.db import get_db
from whiteboard.decorators import is_defined
from whiteboard.descriptors import Id, Name
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import is_user_exists


def is_tag_exists(func):
    """
    Decorator to check wheather the tag object with id exists.

    :param objects: Objects to be checked for existence.
    """

    def _decorator(*args, **kwargs):
        logger.debug("Check if tag exists.")
        try:
            tag_id = getattr(args[0], "tag_id")
        except AttributeError as exc:
            raise InvalidAttributeError("tag_id") from exc
        if not Tag.exist_tag_id(tag_id):
            raise NotFoundError(Tag.__name__, tag_id)
        return func(*args, **kwargs)

    return _decorator


def is_owner(func):
    """
    Decorator to check wheather the workout is owned by user.
    """

    def _decorator(*args, **kwargs):
        # @todo
        return func(*args, **kwargs)

    return _decorator


class Tag:

    tag_id = Id()
    user_id = Id()
    name = Name()

    def __init__(
        self,
        tag_id: Optional[int] = None,
        user_id: Optional[int] = None,
        name: Optional[str] = None,
    ) -> None:
        self.tag_id = tag_id
        self.user_id = user_id
        self.name = name

    def __str__(self):
        return (
            f"Tag ( tag_id={self.tag_id}, user_id={self.user_id},"
            f" name={self.name} )"
        )

    def to_json(self):
        return json.dumps(self.__dict__)

    @property
    def db(self):
        return get_db()

    @property
    def id(self):
        return self.tag_id

    @staticmethod
    def _query_to_object(query: sqlite3.Row) -> Union[Tag, None]:
        """Create tag instance based on the query."""
        if query is None:
            return None

        return Tag(
            query["id"],  # id=tag_id
            query["userId"],
            query["tag"],  # name=tag
        )

    @staticmethod
    def exist_tag_id(tag_id: int) -> bool:
        """
        Check if tag with tag id exists by requesting them.

        :param: tag id
        :return: True if tag with tag id exists, otherwise False.
        :rtype: bool
        """
        result = (
            get_db()
            .execute("SELECT id FROM table_tags WHERE id = ?", (tag_id,))
            .fetchone()
        )

        if result is None:
            return False

        return True

    @is_defined(attributes=("tag_id", "user_id"))
    @is_user_exists
    def get(self) -> Tag:
        """
        Get tag from db by tag_id and user_id.

        :return: Tag object
        :rtype: Tag
        """
        result = self.db.execute(
            """SELECT id, userId, tag FROM table_tags
            WHERE id = ? AND ( userId = 1 OR userId = ? )""",
            (self.tag_id, self.user_id),
        ).fetchone()

        tag = Tag._query_to_object(result)
        if tag is None:
            raise NotFoundError(type(self).__name__, self.tag_id)

        return tag

    @is_defined(attributes=("user_id", "name"))
    @is_user_exists
    def add(self) -> int:
        """
        Add new tag to db.

        :return: Return the id of the created tag.
        :rtype: int
        """
        self.db.execute(
            "INSERT INTO table_tags (userId, tag) VALUES (?, ?)",
            (
                self.user_id,
                self.name,
            ),
        )
        self.db.commit()
        inserted_id = self.db.execute(
            "SELECT last_insert_rowid() FROM table_tags WHERE userId = ? LIMIT 1",
            (self.user_id,),
        ).fetchone()

        try:
            return int(inserted_id["last_insert_rowid()"])
        except (TypeError, ValueError) as e:
            logger.error("Invalid last_insert_rowid: %s" % e)
            raise

    @is_defined(attributes=("tag_id", "user_id", "name"))
    @is_tag_exists
    @is_user_exists
    def update(self) -> bool:
        """
        Update tag in db by id.

        :return: True if tag was updated.
        :rtype: bool
        """
        self.db.execute(
            "UPDATE table_tags SET tag = ? WHERE id = ? AND userId = ?",
            (
                self.name,
                self.tag_id,
                self.user_id,
            ),
        )
        self.db.commit()

        return True

    @is_defined(attributes=("tag_id", "user_id"))
    @is_tag_exists
    @is_user_exists
    def remove(self) -> bool:
        """
        Remove tag from db by id.

        :return: True if tag was removed.
        :rtype: bool
        """
        # @todo: Remove Connection between tags and tags too
        self.db.execute(
            "DELETE FROM table_tags WHERE id = ? AND userId = ?",
            (
                self.tag_id,
                self.user_id,
            ),
        )
        self.db.commit()

        return True
