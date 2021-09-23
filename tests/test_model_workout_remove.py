import pytest

from whiteboard.exceptions import (
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidIdError,
    WorkoutNotFoundError,
)
from whiteboard.models.workout import Workout


@pytest.mark.parametrize(('workout_id'), (
    (1), (1.0), ('1'),
))
def test_remove_workout__valid_workout_id(app, workout_id):
    """Test remove() from workout model with valid data."""
    with app.app_context():
        _workout = Workout(workout_id, 1, 'test_name', 'workout description')
        result = _workout.remove()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_remove_workout__valid_user_id(app, user_id):
    """Test remove() from workout model with valid data."""
    with app.app_context():
        _workout = Workout(1, user_id, 'test_name', 'workout description')
        result = _workout.remove()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_workout__invalid_workout_id(app, workout_id):
    """Test remove() from workout model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _workout = Workout(workout_id, 1, 'test_name',
                               'workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_remove_workout__not_found_workout_id(app, workout_id):
    """
    Test remove() from workout model with an workout id that does not exist.
    """
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _workout = Workout(workout_id, 1, 'test_name',
                               'workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_workout__invalid_user_id(app, user_id):
    """Test remove() from workout model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _workout = Workout(1, user_id, 'test_name',
                               'workout description')
            result = _workout.remove()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_remove_workout__not_found_user_id(app, user_id):
    """Test remove() from workout model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _workout = Workout(1, user_id, 'test_name',
                               'workout description')
            result = _workout.remove()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'
