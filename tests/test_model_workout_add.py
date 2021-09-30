from whiteboard.exceptions import (
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidDatetimeError,
    WorkoutInvalidDescriptionError,
    WorkoutInvalidNameError,
)
from whiteboard.models.workout import Workout

import pytest


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_add_workout__valid(app, user_id):
    """Test add() from workout model with valid data (no datetime)."""
    with app.app_context():
        _workout = Workout(None, user_id, 'test name', 'test description')
        workout_id = _workout.add()
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


@pytest.mark.parametrize(('workout_datetime'), (
    (123), ('123'),
))
def test_add_workout__valid_with_datetime(app, workout_datetime):
    """Test add() from workout model with valid data (with datetime)."""
    with app.app_context():
        _workout = Workout(None, 1, 'test name',
                           'test description', workout_datetime)
        workout_id = _workout.add()
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_workout__invalid_user_id(app, user_id):
    """Test add() from workout model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _workout = Workout(None, user_id, 'test name', 'test description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_add_workout__not_found_user_id(app, user_id):
    """Test add() from workout model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _workout = Workout(None, user_id, 'test name',
                               'workout description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_workout__invalid_name(app, workout_name):
    """Test add() from workout model with invalid workout name."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidNameError) as e:
            _workout = Workout(None, 1, workout_name, 'test description')
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid workout name.'


@pytest.mark.parametrize(('workout_description'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_workout__invalid_description(app, workout_description):
    """Test add() from workout model with invalid workout description."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidDescriptionError) as e:
            _workout = Workout(None, 1, 'test name', workout_description)
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid workout description.'


@pytest.mark.parametrize(('workout_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_add_workout__invalid_datetime(app, workout_datetime):
    """Test add() from workout model with invalid workout datetime."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidDatetimeError) as e:
            _workout = Workout(None, 1, 'test name',
                               'workout description', workout_datetime)
            workout_id = _workout.add()
            assert workout_id is None
        assert str(e.value) == 'Invalid workout datetime.'
