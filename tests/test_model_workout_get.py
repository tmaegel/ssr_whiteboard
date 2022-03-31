# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout


@pytest.mark.parametrize(
    ("workout_id"),
    (
        (1),
        ("1"),
    ),
)
def test_get_workout__valid_workout_id(app, workout_id):
    """Test get() from workout model with valid workout_id."""
    with app.app_context():
        _workout = Workout(workout_id=workout_id, user_id=1)
        workout = _workout.get()
        assert workout is not None
        assert workout.workout_id == int(workout_id)
        assert workout.user_id == 1
        assert workout.name == "Workout A from admin"
        assert workout.description == "Workout A description from admin"
        assert workout.datetime == 0


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_get_workout__valid_user_id(app, user_id):
    """Test get() from workout model with valid user_id."""
    with app.app_context():
        _workout = Workout(workout_id=1, user_id=user_id)
        workout = _workout.get()
        assert workout is not None
        assert workout.workout_id == 1
        assert workout.user_id == int(user_id)
        assert workout.name == "Workout A from admin"
        assert workout.description == "Workout A description from admin"
        assert workout.datetime == 0


def test_get_workout__not_owner(app, workout_id_user, user_id_admin):
    """
    Test get() from workout model with workout that does
    not belong to the user.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id_user, user_id=user_id_admin)
            result = _workout.get()
            assert result is None
        assert str(e.value) == (f"Workout with id {workout_id_user} does not exist.")


@pytest.mark.parametrize(("workout_id"), ((99999),))
def test_get_workout__not_found_workout_id(app, workout_id):
    """Test get() from workout model with workout_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == f"Workout with id {workout_id} does not exist."


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_get_workout__not_found_user_id(app, user_id):
    """Test get() from workout model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _workout = Workout(workout_id=1, user_id=user_id)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == f"User with id {user_id} does not exist."


@pytest.mark.parametrize(
    ("workout_id"),
    (
        (0),
        (-1),
        (1.0),
        ("1.0"),
        (None),
        ("abc"),
        (True),
        (False),
    ),
)
def test_get_workout__invalid_workout_id(app, workout_id):
    """Test get() from workout model with invalid workout_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=workout_id, user_id=1)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == "Invalid workout_id."


@pytest.mark.parametrize(
    ("user_id"),
    (
        (0),
        (-1),
        (1.0),
        ("1.0"),
        (None),
        ("abc"),
        (True),
        (False),
    ),
)
def test_get_workout__invalid_user_id(app, user_id):
    """Test get() from workout model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _workout = Workout(workout_id=1, user_id=user_id)
            workout = _workout.get()
            assert workout is None
        assert str(e.value) == "Invalid user_id."
