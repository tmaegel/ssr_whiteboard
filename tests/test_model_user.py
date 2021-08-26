import pytest
from whiteboard.exceptions import (
    UserNotFoundError,
    UserNoneObjectError,
    UserInvalidIdError,
    UserInvalidNameError,
    UserInvalidPasswordError,
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

#
# User.add()
#


def test_add_user__valid(app):
    """Test add() from user model with valid data."""
    user = User(
        None,
        'test name',
        'test password'
    )
    with app.app_context():
        user = User.add(user)
        assert user is not None
        assert isinstance(user, str) is True


def test_add_user__invalid_object(app):
    """Test add() from user model with invalid object."""
    with app.app_context():
        with pytest.raises(UserNoneObjectError) as e:
            user = User.add(None)
            assert user is None
        assert str(e.value) == 'User object is None.'


@pytest.mark.parametrize(('user_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_user__invalid_name(app, user_name):
    """Test add() from user model with invalid user name."""
    user = User(
        None,
        user_name,
        'test password'
    )
    with app.app_context():
        with pytest.raises(UserInvalidNameError) as e:
            user = User.add(user)
            assert user is None
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
    user = User(
        None,
        'test name',
        user_password
    )
    with app.app_context():
        with pytest.raises(UserInvalidPasswordError) as e:
            user = User.add(user)
            assert user is None
        assert str(e.value) == 'Invalid user password.'


#
# User.update()
#


def test_update_user__valid(app):
    """Test update() from user model with valid data."""
    user = User(
        1,
        'test name',
        'test password'
    )
    with app.app_context():
        user_id = User.update(user)
        assert user_id is not None
        assert isinstance(user_id, int) is True


def test_update_user__invalid_object(app):
    """Test update() from user model with invalid object."""
    with app.app_context():
        with pytest.raises(UserNoneObjectError) as e:
            user_id = User.update(None)
            assert user_id is None
        assert str(e.value) == 'User object is None.'


@pytest.mark.parametrize(('user_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_user__invalid_name(app, user_name):
    """Test update() from user model with invalid user name."""
    user = User(
        1,
        user_name,
        'test password'
    )
    with app.app_context():
        with pytest.raises(UserInvalidNameError) as e:
            user_id = User.update(user)
            assert user_id is None
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
    user = User(
        1,
        'test name',
        user_password
    )
    with app.app_context():
        with pytest.raises(UserInvalidPasswordError) as e:
            user_id = User.update(user)
            assert user_id is None
        assert str(e.value) == 'Invalid user password.'
