from whiteboard.exceptions import (
    UserInvalidIdError,
    UserInvalidNameError,
    UserNotFoundError,
)
from whiteboard.models.user import User

import pytest


@pytest.mark.parametrize(('user_id', 'user_name'), (
    (1, 'admin'),
    ('1', 'admin'),
    (1.0, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_id__valid(app, user_id, user_name):
    """Test get() from user model with valid data."""
    with app.app_context():
        _user = User(user_id, None, None)
        user = _user.get()
        assert user is not None
        assert user.user_id == int(user_id)
        assert user.name == user_name


@pytest.mark.parametrize(('user_id', 'user_name'), (
    (1, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_name__valid(app, user_id, user_name):
    """Test get_by_name() from user model with valid data."""
    with app.app_context():
        _user = User(None, user_name, None)
        user = _user.get_by_name()
        assert user is not None
        assert user.user_id == user_id
        assert user.name == user_name


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_get_user__not_found_user_id(app, user_id):
    """Test get() from user model with an id that does not exist."""
    with app.app_context():
        _user = User(user_id, None, None)
        with pytest.raises(UserNotFoundError) as e:
            user = _user.get()
            assert user is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('user_name'), (
    ('admin1'), ('test3'), ('Admin'),
))
def test_get_user__not_found_name(app, user_name):
    """Test get_by_name() from user model with an name that does not exist."""
    with app.app_context():
        _user = User(None, user_name, None)
        with pytest.raises(UserNotFoundError) as e:
            user = _user.get_by_name()
            assert user is None
        assert str(
            e.value) == f'User with id or name {user_name} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_user__invalid(app, user_id):
    """Test get() from user model with invalid data."""
    with app.app_context():
        _user = User(user_id, None, None)
        with pytest.raises(UserInvalidIdError) as e:
            user = _user.get()
            assert user is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_get_user_by_name__invalid(app, user_name):
    """Test get_by_name() from user model with invalid data."""
    with app.app_context():
        _user = User(None, user_name, None)
        with pytest.raises(UserInvalidNameError) as e:
            user = _user.get_by_name()
            assert user is None
        assert str(e.value) == 'Invalid user name.'
