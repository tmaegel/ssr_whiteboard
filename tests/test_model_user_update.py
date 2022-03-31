# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import User


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_update_user__valid_user_id(app, user_id):
    """Test update() from user model with valid data."""
    with app.app_context():
        _user = User(user_id=user_id, name="test name", password_hash="test password")
        result = _user.update()
        assert result is True


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_update_user__not_found_user_id(app, user_id):
    """Test update() from user model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _user = User(
                user_id=user_id, name="test_name", password_hash="test password"
            )
            result = _user.update()
            assert result is None
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
def test_update_user__invalid_user_id(app, user_id):
    """Test update() from user model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(
                user_id=user_id, name="test_name", password_hash="test password"
            )
            result = _user.update()
            assert result is None
        assert str(e.value) == "Invalid user_id."


@pytest.mark.parametrize(
    ("user_name"),
    (
        (123),
        (123.42),
        (True),
        ([]),
        (None),
    ),
)
def test_update_user__invalid_name(app, user_name):
    """Test update() from user model with invalid name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(user_id=1, name=user_name, password_hash="test password")
            result = _user.update()
            assert result is None
        assert str(e.value) == "Invalid name."


@pytest.mark.parametrize(
    ("user_password"),
    (
        (123),
        (123.42),
        (True),
        ([]),
        (None),
    ),
)
def test_update_user__invalid_password(app, user_password):
    """Test update() from user model with invalid password_hash."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(user_id=1, name="test name", password_hash=user_password)
            result = _user.update()
            assert result is None
        assert str(e.value) == "Invalid password_hash."
