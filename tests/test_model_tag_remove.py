# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.tag import Tag


@pytest.mark.parametrize(
    ("tag_id"),
    (
        (1),
        ("1"),
    ),
)
def test_remove_tag__valid_tag_id(app, tag_id):
    """Test remove() from tag model with valid tag_id."""
    with app.app_context():
        _tag = Tag(tag_id=tag_id, user_id=1, name="tag name")
        result = _tag.remove()
        assert result is True


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_remove_tag__valid_user_id(app, user_id):
    """Test remove() from tag model with valid user_id."""
    with app.app_context():
        _tag = Tag(tag_id=1, user_id=user_id, name="tag name")
        result = _tag.remove()
        assert result is True


@pytest.mark.parametrize(("tag_id"), ((99999),))
def test_remove_tag__not_found_tag_id(app, tag_id):
    """Test remove() from tag model with tag_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _tag = Tag(tag_id=tag_id, user_id=1, name="tag name")
            result = _tag.remove()
            assert result is None
        assert str(e.value) == f"Tag with id {tag_id} does not exist."


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_remove_tag__not_found_user_id(app, user_id):
    """Test remove() from tag model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _tag = Tag(tag_id=1, user_id=user_id, name="tag name")
            result = _tag.remove()
            assert result is None
        assert str(e.value) == f"User with id {user_id} does not exist."


@pytest.mark.parametrize(
    ("tag_id"),
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
def test_remove_tag__invalid_tag_id(app, tag_id):
    """Test remove() from tag model with invalid tag_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _tag = Tag(tag_id=tag_id, user_id=1, name="tag name")
            result = _tag.remove()
            assert result is None
        assert str(e.value) == "Invalid tag_id."


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
def test_remove_tag__invalid_user_id(app, user_id):
    """Test remove() from tag model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _tag = Tag(tag_id=1, user_id=user_id, name="tag name")
            result = _tag.remove()
            assert result is None
        assert str(e.value) == "Invalid user_id."
