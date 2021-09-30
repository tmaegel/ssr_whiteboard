# -*- coding: utf-8 -*-
from whiteboard.exceptions import WorkoutInvalidIdError, WorkoutNotFoundError
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), (1.0), ('1'),
))
def test_get_workout__valid(app, workout_id):
    """Test get() from workout model with valid data."""
    with app.app_context():
        _workout = Workout(workout_id, None, None, None)
        workout = _workout.get()
        assert workout is not None
        assert workout.workout_id == int(workout_id)
        assert workout.user_id == 1
        assert workout.name == 'Workout A from admin'
        assert workout.description == 'Workout A description from admin'
        assert workout.datetime == 0


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_get_workout__not_found_workout_id(app, workout_id):
    """Test get() from workout model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _workout = Workout(workout_id, None, None, None)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_workout__invalid(app, workout_id):
    """Test get() from workout model with invalid data."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _workout = Workout(workout_id, None, None, None)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == 'Invalid workout id.'
