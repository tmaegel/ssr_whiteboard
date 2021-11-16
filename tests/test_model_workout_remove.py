# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), ('1'),
))
def test_remove_workout__valid_workout_id(app, workout_id):
    """Test remove() from workout model with valid workout_id."""
    with app.app_context():
        _workout = Workout(workout_id=workout_id, user_id=1,
                           name='test_name', description='workout description')
        result = _workout.remove()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_remove_workout__valid_user_id(app, user_id):
    """Test remove() from workout model with valid user_id."""
    with app.app_context():
        _workout = Workout(workout_id=1, user_id=user_id,
                           name='test_name', description='workout description')
        result = _workout.remove()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (99999),
))
def test_remove_workout__not_found_workout_id(app, workout_id):
    """
    Test remove() from workout model with workout_id that does not exist.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1,
                               name='test_name',
                               description='workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_remove_workout__not_found_user_id(app, user_id):
    """Test remove() from workout model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=1, user_id=user_id,
                               name='test_name',
                               description='workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_workout__invalid_workout_id(app, workout_id):
    """Test remove() from workout model with invalid workout_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1,
                               name='test_name',
                               description='workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == 'Invalid workout_id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_workout__invalid_user_id(app, user_id):
    """Test remove() from workout model with invalid user id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=user_id,
                               name='test_name',
                               description='workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == 'Invalid user_id.'
