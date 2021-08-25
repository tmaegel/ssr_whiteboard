import pytest
from whiteboard.exceptions import (
    UserNotFoundError,
    UserInvalidIdError,
    UserInvalidNameError,
)
from whiteboard.models.user import (
    User,
)

#
# User.get()
#


@pytest.mark.parametrize(('user_id', 'name'), (
    (1, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_id__valid(app, user_id, name):
    """Test get() from user model with valid data."""
    with app.app_context():
        user = User.get(user_id=user_id)
        assert user is not None
        assert user.id == user_id
        assert user.name == name


@pytest.mark.parametrize(('user_id', 'name'), (
    (1, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_name__valid(app, user_id, name):
    """Test get_by_name() from user model with valid data."""
    with app.app_context():
        user = User.get_by_name(name=name)
        assert user is not None
        assert user.id == user_id
        assert user.name == name


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_get_user__not_exist(app, user_id):
    """Test get() from user model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            user = User.get(user_id)
            assert user is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('name'), (
    ('admin1'),
    ('test3'),
    ('Admin'),
))
def test_get_user_by_name__not_exist(app, name):
    """Test get_by_name() from user model with an name that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            user = User.get_by_name(name=name)
            assert user is None
        assert str(
            e.value) == f'User with id or name {name} does not exist.'


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
        with pytest.raises(UserInvalidIdError) as e:
            user = User.get(user_id)
            assert user is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_get_user_by_name__invalid(app, name):
    """Test get_by_name() from user model with invalid data."""
    with app.app_context():
        with pytest.raises(UserInvalidNameError) as e:
            user = User.get_by_name(name=name)
            assert user is None
        assert str(e.value) == 'Invalid user name.'
