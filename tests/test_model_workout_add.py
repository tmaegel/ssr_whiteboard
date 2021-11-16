# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_add_workout__valid_user_id(app, user_id):
    """Test add() from workout model with valid user_id (no datetime)."""
    with app.app_context():
        _workout = Workout(user_id=user_id, name='test name',
                           description='test description')
        workout_id = _workout.add()
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


@pytest.mark.parametrize(('workout_datetime'), (
    (123), ('123'),
))
def test_add_workout__valid_with_datetime(app, workout_datetime):
    """Test add() from workout model with valid data (with datetime)."""
    with app.app_context():
        _workout = Workout(user_id=1, name='test name',
                           description='test description',
                           datetime=workout_datetime)
        workout_id = _workout.add()
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_workout__invalid_user_id(app, user_id):
    """Test add() from workout model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(user_id=user_id, name='test name',
                               description='test description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid user_id.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_add_workout__not_found_user_id(app, user_id):
    """Test add() from workout model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(user_id=user_id, name='test name',
                               description='workout description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('workout_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_workout__invalid_name(app, workout_name):
    """Test add() from workout model with invalid workout name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(user_id=1, name=workout_name,
                               description='test description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid name.'


@pytest.mark.parametrize(('workout_description'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_workout__invalid_description(app, workout_description):
    """Test add() from workout model with invalid workout description."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(user_id=1, name='test name',
                               description=workout_description)
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid description.'


@pytest.mark.parametrize(('workout_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_add_workout__invalid_datetime(app, workout_datetime):
    """Test add() from workout model with invalid workout datetime."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(user_id=1, name='test name',
                               description='workout description',
                               datetime=workout_datetime)
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid datetime.'
