import pytest

from whiteboard.exceptions import (
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
    UserNotFoundError,
)
from whiteboard.models.user import User

#
# User.get()
#


@pytest.mark.parametrize(('user_id', 'user_name'), (
    (1, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_id__valid(app, user_id, user_name):
    """Test get() from user model with valid data."""
    with app.app_context():
        _user = User(user_id, None, None)
        user = _user.get()
        assert user is not None
        assert user.user_id == user_id
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
    (0),
    (99999),
))
def test_get_user__not_exist(app, user_id):
    """Test get() from user model with an id that does not exist."""
    with app.app_context():
        _user = User(user_id, None, None)
        with pytest.raises(UserNotFoundError) as e:
            user = _user.get()
            assert user is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('user_name'), (
    ('admin1'),
    ('test3'),
    ('Admin'),
))
def test_get_user_by_name__not_exist(app, user_name):
    """Test get_by_name() from user model with an name that does not exist."""
    with app.app_context():
        _user = User(None, user_name, None)
        with pytest.raises(UserNotFoundError) as e:
            user = _user.get_by_name()
            assert user is None
        assert str(
            e.value) == f'User with id or name {user_name} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    ('1'),
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
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
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_get_user_by_name__invalid(app, user_name):
    """Test get_by_name() from user model with invalid data."""
    with app.app_context():
        _user = User(None, user_name, None)
        with pytest.raises(UserInvalidNameError) as e:
            user = _user.get_by_name()
            assert user is None
        assert str(e.value) == 'Invalid user name.'

#
# User.add()
#


def test_add_user__valid(app):
    """Test add() from user model with valid data."""
    with app.app_context():
        _user = User(None, 'test name', 'test password')
        result = _user.add()
        assert result is True


@pytest.mark.parametrize(('user_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
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
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_user__invalid_password(app, user_password):
    """Test add() from user model with invalid user password."""
    with app.app_context():
        _user = User(None, 'test name', user_password)
        with pytest.raises(UserInvalidPasswordError) as e:
            result = _user.add()
            assert result is None
        assert str(e.value) == 'Invalid user password.'


#
# User.update()
#


def test_update_user__valid(app):
    """Test update() from user model with valid data."""
    with app.app_context():
        _user = User(1, 'test name', 'test password')
        result = _user.update()
        assert result is True


@pytest.mark.parametrize(('user_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
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
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_user__invalid_password(app, user_password):
    """Test update() from user model with invalid user password."""
    with app.app_context():
        _user = User(1, 'test name', user_password)
        with pytest.raises(UserInvalidPasswordError) as e:
            result = _user.update()
            assert result is None
        assert str(e.value) == 'Invalid user password.'
