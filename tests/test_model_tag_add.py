# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.tag import Tag


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_add_tag__valid_user_id(app, user_id):
    """Test add() from tag model with valid user_id"""
    with app.app_context():
        _tag = Tag(user_id=user_id, name="tag name")
        tag_id = _tag.add()
        assert tag_id is not None
        assert isinstance(tag_id, int) is True


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_add_tag__not_found_user_id(app, user_id):
    """Test add() from tag model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _tag = Tag(user_id=user_id, name="tag name")
            tag_id = _tag.add()
            assert tag_id is None
        assert str(e.value) == f"User with id {user_id} does not exist."


@pytest.mark.parametrize(
    ("user_id"),
    (
        (0),
        (-1),
        (1.0),
        ("1.0"),
        (None),
        ("abc"),
        (True),
        (False),
    ),
)
def test_add_tag__invalid_user_id(app, user_id):
    """Test add() from tag model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _tag = Tag(user_id=user_id, name="tag name")
            tag_id = _tag.add()
            assert tag_id is None
        assert str(e.value) == "Invalid user_id."


@pytest.mark.parametrize(
    ("tag_name"),
    (
        (123),
        (123.42),
        (True),
        ([]),
        (None),
    ),
)
def test_add_tag__invalid_name(app, tag_name):
    """Test add() from tag model with invalid tag name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _tag = Tag(user_id=1, name=tag_name)
            tag_id = _tag.add()
            assert tag_id is None
        assert str(e.value) == "Invalid name."
