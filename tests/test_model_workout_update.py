from whiteboard.exceptions import (
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidDatetimeError,
    WorkoutInvalidDescriptionError,
    WorkoutInvalidIdError,
    WorkoutInvalidNameError,
    WorkoutNotFoundError,
)
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('workout_id'), (
    (1), (1.0), ('1'),
))
def test_update_workout__valid_workout_id(app, workout_id):
    """Test update() from workout model with valid data (no datetime)."""
    with app.app_context():
        _workout = Workout(workout_id, 1, 'test name', 'workout description')
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_update_workout__valid_user_id(app, user_id):
    """Test update() from workout model with valid data (no datetime)."""
    with app.app_context():
        _workout = Workout(1, user_id, 'test name', 'workout description')
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('workout_datetime'), (
    (123), ('123'),
))
def test_update_workout__valid_with_datetime(app, workout_datetime):
    """Test update() from workout model with valid data (with datetime)."""
    with app.app_context():
        _workout = Workout(1, 1, 'test name',
                           'workout description', workout_datetime)
        result = _workout.update()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_workout__invalid_workout_id(app, workout_id):
    """Test update() from workout model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _workout = Workout(workout_id, 1, 'test name',
                               'workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_update_workout__not_found_workout_id(app, workout_id):
    """
    Test update() from workout model with an workout id that does not exist.
    """
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _workout = Workout(workout_id, 1, 'test_name',
                               'workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_workout__invalid_user_id(app, user_id):
    """Test update() from workout model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _workout = Workout(1, user_id, 'test name',
                               'workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_update_workout__not_found_user_id(app, user_id):
    """Test update() from workout model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _workout = Workout(1, user_id, 'test_name',
                               'workout description')
            result = _workout.update()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_name'), (
    (123), (123.42), (True), (False), ([]), (None),
))
def test_update_workout__invalid_name(app, workout_name):
    """Test update() from workout model with invalid workout name."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidNameError) as e:
            _workout = Workout(1, 1, workout_name,
                               'workout description')
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid workout name.'


@pytest.mark.parametrize(('workout_description'), (
    (123), (123.42), (True), (False), ([]), (None),
))
def test_update_workout__invalid_description(app, workout_description):
    """Test update() from workout model with invalid workout description."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidDescriptionError) as e:
            _workout = Workout(1, 1, 'test_name',
                               workout_description)
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid workout description.'


@pytest.mark.parametrize(('workout_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_update_workout__invalid_datetime(app, workout_datetime):
    """Test update() from workout model with invalid workout datetime."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidDatetimeError) as e:
            _workout = Workout(1, 1, 'test_name',
                               'workout description', workout_datetime)
            result = _workout.update()
            assert result is None
        assert str(e.value) == 'Invalid workout datetime.'
