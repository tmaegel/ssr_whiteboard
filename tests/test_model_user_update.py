import pytest

from whiteboard.exceptions import (
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
    UserNotFoundError,
)
from whiteboard.models.user import User


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'), (1.0),
))
def test_update_user__valid(app, user_id):
    """Test update() from user model with valid data."""
    with app.app_context():
        _user = User(user_id, 'test name', 'test password')
        result = _user.update()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_user__invalid_user_id(app, user_id):
    """Test update() from user model with invalid user id."""
    with app.app_context():
        _user = User(user_id, 'test_name', 'test password')
        with pytest.raises(UserInvalidIdError) as e:
            result = _user.update()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_update_user__invalid_name(app, user_name):
    """Test update() from user model with invalid user name."""
    with app.app_context():
        _user = User(1, user_name, 'test password')
        with pytest.raises(UserInvalidNameError) as e:
            result = _user.update()
            assert result is None
        assert str(e.value) == 'Invalid user name.'


@pytest.mark.parametrize(('user_password'), (
    (123), (123.42), (True), ([]), (None),
))
def test_update_user__invalid_password(app, user_password):
    """Test update() from user model with invalid user password."""
    with app.app_context():
        _user = User(1, 'test name', user_password)
        with pytest.raises(UserInvalidPasswordError) as e:
            result = _user.update()
            assert result is None
        assert str(e.value) == 'Invalid user password.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_update_user__not_found_user_id(app, user_id):
    """Test update() from user model with an user id that does not exist."""
    with app.app_context():
        _user = User(user_id, 'test_name', 'test password')
        with pytest.raises(UserNotFoundError) as e:
            result = _user.update()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'
