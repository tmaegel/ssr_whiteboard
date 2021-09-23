import pytest

from whiteboard.exceptions import (
    UserInvalidNameError,
    UserInvalidPasswordError,
)
from whiteboard.models.user import User


def test_add_user__valid(app):
    """Test add() from user model with valid data."""
    with app.app_context():
        _user = User(None, 'test name', 'test password')
        result = _user.add()
        assert result is True


@pytest.mark.parametrize(('user_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_user__invalid_name(app, user_name):
    """Test add() from user model with invalid user name."""
    with app.app_context():
        _user = User(None, user_name, 'test password')
        with pytest.raises(UserInvalidNameError) as e:
            result = _user.add()
            assert result is None
        assert str(e.value) == 'Invalid user name.'


@pytest.mark.parametrize(('user_password'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_user__invalid_password(app, user_password):
    """Test add() from user model with invalid user password."""
    with app.app_context():
        _user = User(None, 'test name', user_password)
        with pytest.raises(UserInvalidPasswordError) as e:
            result = _user.add()
            assert result is None
        assert str(e.value) == 'Invalid user password.'
