# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError
from whiteboard.models.user import User


def test_add_user__valid_user_id(app):
    """Test add() from user model with valid user_id."""
    with app.app_context():
        _user = User(name="test name", password_hash="test password")
        user_id = _user.add()
        assert user_id is not None
        assert isinstance(user_id, int) is True


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
def test_add_user__invalid_name(app, user_name):
    """Test add() from user model with invalid user name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(None, user_name, "test password")
            result = _user.add()
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
def test_add_user__invalid_password(app, user_password):
    """Test add() from user model with invalid user password."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(name="test name", password_hash=user_password)
            result = _user.add()
            assert result is None
        assert str(e.value) == "Invalid password_hash."
