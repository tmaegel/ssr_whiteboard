# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), ('1'),
))
def test_update_workout__valid_workout_id(app, workout_id):
    """Test update() from workout model with valid workout_id (no datetime)."""
    with app.app_context():
        _workout = Workout(workout_id=workout_id, user_id=1,
                           name='test name', description='workout description')
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_update_workout__valid_user_id(app, user_id):
    """Test update() from workout model with valid user_id (no datetime)."""
    with app.app_context():
        _workout = Workout(workout_id=1, user_id=user_id,
                           name='test name', description='workout description')
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('workout_datetime'), (
    (123), ('123'),
))
def test_update_workout__valid_with_datetime(app, workout_datetime):
    """Test update() from workout model with valid data (with datetime)."""
    with app.app_context():
        _workout = Workout(workout_id=1, user_id=1,
                           name='test name', description='workout description',
                           datetime=workout_datetime)
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (99999),
))
def test_update_workout__not_found_workout_id(app, workout_id):
    """
    Test update() from workout model with workout_id that does not exist.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1,
                               name='test name',
                               description='workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_update_workout__not_found_user_id(app, user_id):
    """Test update() from workout model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=1, user_id=user_id,
                               name='test name',
                               description='workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_workout__invalid_workout_id(app, workout_id):
    """Test update() from workout model with invalid workout id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1,
                               name='test name',
                               description='workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid workout_id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_workout__invalid_user_id(app, user_id):
    """Test update() from workout model with invalid user id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=user_id,
                               name='test name',
                               description='workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid user_id.'


@pytest.mark.parametrize(('workout_name'), (
    (123), (123.42), (True), (False), ([]), (None),
))
def test_update_workout__invalid_name(app, workout_name):
    """Test update() from workout model with invalid workout name."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=1,
                               name=workout_name,
                               description='workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid name.'


@pytest.mark.parametrize(('workout_description'), (
    (123), (123.42), (True), (False), ([]), (None),
))
def test_update_workout__invalid_description(app, workout_description):
    """Test update() from workout model with invalid workout description."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=1,
                               name='test name',
                               description=workout_description)
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid description.'


@pytest.mark.parametrize(('workout_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_update_workout__invalid_datetime(app, workout_datetime):
    """Test update() from workout model with invalid workout datetime."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=1,
                               name='test name',
                               description='workout description',
                               datetime=workout_datetime)
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid datetime.'
