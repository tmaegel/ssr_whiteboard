# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.workout import Workout


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_get_workout__valid_user_id(app, user_id):
    """Test list() from workout model with valid user_id."""
    with app.app_context():
        results = Workout.list(user_id=user_id)
        assert results is not None
        assert isinstance(results, list) is True
        assert len(results) > 0
        for attr in ("workout_id", "user_id", "name", "description", "datetime"):
            assert hasattr(results[0], attr) is True


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
def test_get_workout__invalid_user(app, user_id):
    """Test list() from workout model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            results = Workout.list(user_id=user_id)
            assert results is None
        assert str(e.value) == "Invalid user_id."


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_get_workout__not_found_user(app, user_id):
    """Test list() from workout model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            results = Workout.list(user_id=user_id)
            assert results is None
        assert str(e.value) == f"User with id {user_id} does not exist."
