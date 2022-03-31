# -*- coding: utf-8 -*-
import pytest

from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.score import Score


@pytest.mark.parametrize(
    ("score_id"),
    (
        (1),
        ("1"),
    ),
)
def test_update_score__valid_score_id(app, score_id):
    """Test update() from score model with valid score_id (no datetime)."""
    with app.app_context():
        _score = Score(
            score_id=score_id,
            user_id=1,
            workout_id=2,
            value="60",
            rx=True,
            note="test note",
        )
        result = _score.update()
        assert result is True


@pytest.mark.parametrize(
    ("user_id"),
    (
        (1),
        ("1"),
    ),
)
def test_update_score__valid_user_id(app, user_id):
    """Test update() from score model with valid user_id (no datetime)."""
    with app.app_context():
        _score = Score(
            score_id=1,
            user_id=user_id,
            workout_id=2,
            value="60",
            rx=True,
            note="test note",
        )
        result = _score.update()
        assert result is True


@pytest.mark.parametrize(
    ("workout_id"),
    (
        (2),
        ("2"),
    ),
)
def test_update_score__valid_workout_id(app, workout_id):
    """Test update() from score model with valid workout_id (no datetime)."""
    with app.app_context():
        _score = Score(
            score_id=1,
            user_id=1,
            workout_id=workout_id,
            value="60",
            rx=True,
            note="test note",
        )
        result = _score.update()
        assert result is True


@pytest.mark.parametrize(
    ("score_datetime"),
    (
        (123),
        ("123"),
    ),
)
def test_update_score__valid_with_datetime(app, score_datetime):
    """Test update() from score model with valid data (with datetime)."""
    with app.app_context():
        _score = Score(
            score_id=1,
            user_id=1,
            workout_id=2,
            value="60",
            rx=True,
            note="test note",
            datetime=score_datetime,
        )
        result = _score.update()
        assert result is True


@pytest.mark.parametrize(("score_id"), ((99999),))
def test_update_score__not_found_score_id(app, score_id):
    """Test update() from score model with score_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(
                score_id=score_id,
                user_id=1,
                workout_id=2,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == f"Score with id {score_id} does not exist."


@pytest.mark.parametrize(("user_id"), ((99999),))
def test_update_score__not_found_user_id(app, user_id):
    """Test update() from score model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(
                score_id=1,
                user_id=user_id,
                workout_id=2,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == f"User with id {user_id} does not exist."


@pytest.mark.parametrize(("workout_id"), ((99999),))
def test_update_score__not_found_workout_id(app, workout_id):
    """
    Test update() from score model with workout_id that does not exist.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=workout_id,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == f"Workout with id {workout_id} does not exist."


@pytest.mark.parametrize(
    ("score_id"),
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
def test_update_score__invalid_score_id(app, score_id):
    """Test update() from score model with invalid score id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=score_id,
                user_id=1,
                workout_id=2,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid score_id."


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
def test_update_score__invalid_user_id(app, user_id):
    """Test update() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=user_id,
                workout_id=2,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid user_id."


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
def test_update_score__invalid_workout_id(app, workout_id):
    """Test update() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=workout_id,
                value="60",
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid workout_id."


@pytest.mark.parametrize(
    ("score_value"),
    (
        (123),
        (123.42),
        (True),
        ([]),
        (None),
    ),
)
def test_update_score__invalid_value(app, score_value):
    """Test update() from score model with invalid score value."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=2,
                value=score_value,
                rx=True,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid value."


@pytest.mark.parametrize(
    ("score_rx"),
    (
        (123),
        (123.42),
        (1),
        (0),
        ([]),
        (None),
    ),
)
def test_update_score__invalid_rx(app, score_rx):
    """Test update() from score model with invalid score rx."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=2,
                value="60",
                rx=score_rx,
                note="test note",
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid rx."


@pytest.mark.parametrize(
    ("score_note"),
    (
        (123),
        (123.42),
        (True),
        ([]),
        (None),
    ),
)
def test_update_score__invalid_note(app, score_note):
    """Test update() from score model with invalid score note."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=2,
                value="60",
                rx=True,
                note=score_note,
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid note."


@pytest.mark.parametrize(
    ("score_datetime"),
    (
        (-1),
        (True),
        ([]),
        ("abc"),
        ("123.45"),
        (123.45),
        (None),
    ),
)
def test_update_score__invalid_datetime(app, score_datetime):
    """Test update() from score model with invalid score datetime."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(
                score_id=1,
                user_id=1,
                workout_id=2,
                value="60",
                rx=True,
                note="test note",
                datetime=score_datetime,
            )
            result = _score.update()
            assert result is None
        assert str(e.value) == "Invalid datetime."
