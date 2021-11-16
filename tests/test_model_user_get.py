# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.user import User

import pytest


@pytest.mark.parametrize(('user_id', 'user_name'), (
    (1, 'admin'),
    ('1', 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_id__valid_user_id(app, user_id, user_name):
    """Test get() from user model with valid user_id."""
    with app.app_context():
        _user = User(user_id=user_id)
        user = _user.get()
        assert user is not None
        assert user.user_id == int(user_id)
        assert user.name == user_name


@pytest.mark.parametrize(('user_id', 'user_name'), (
    (1, 'admin'),
    (2, 'test1'),
    (3, 'test2'),
))
def test_get_user_by_name__valid_name(app, user_id, user_name):
    """Test get_by_name() from user model with valid name."""
    with app.app_context():
        _user = User(name=user_name)
        user = _user.get_by_name()
        assert user is not None
        assert user.user_id == int(user_id)
        assert user.name == user_name


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_get_user__not_found_user_id(app, user_id):
    """Test get() from user model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _user = User(user_id=user_id)
            user = _user.get()
            assert user is None
        assert str(
            e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('user_name'), (
    ('admin1'), ('test3'), ('Admin'),
))
def test_get_user__not_found_name(app, user_name):
    """Test get_by_name() from user model with name that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _user = User(name=user_name)
            user = _user.get_by_name()
            assert user is None
        assert str(
            e.value) == f'User with id {user_name} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_user__invalid_user_id(app, user_id):
    """Test get() from user model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(user_id=user_id)
            user = _user.get()
            assert user is None
        assert str(e.value) == 'Invalid user_id.'


@pytest.mark.parametrize(('user_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_get_user_by_name__invalid_name(app, user_name):
    """Test get_by_name() from user model with invalid name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _user = User(name=user_name)
            user = _user.get_by_name()
            assert user is None
        assert str(e.value) == 'Invalid name.'
