# -*- coding: utf-8 -*-
from whiteboard.exceptions import (
    ScoreInvalidDatetimeError,
    ScoreInvalidNoteError,
    ScoreInvalidRxError,
    ScoreInvalidValueError,
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidIdError,
    WorkoutNotFoundError,
)
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_add_score__valid_user_id(app, user_id):
    """Test add() from score model with valid data (no datetime)."""
    with app.app_context():
        _score = Score(None, user_id, 2, '60', True, 'test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('workout_id'), (
    (1), (1.0), ('1'),
))
def test_add_score__valid_workout_id(app, workout_id):
    """Test add() from score model with valid data (no datetime)."""
    with app.app_context():
        _score = Score(None, 1, workout_id, '60', True, 'test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('score_datetime'), (
    (123), ('123'),
))
def test_add_score__valid_with_datetime(app, score_datetime):
    """Test add() from score model with valid data (no datetime)."""
    with app.app_context():
        _score = Score(None, 1, 2, '60', True, 'test note', score_datetime)
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_score__invalid_user_id(app, user_id):
    """Test add() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _score = Score(None, user_id, 2, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_add_score__not_found_user_id(app, user_id):
    """Test add() from score model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _score = Score(None, user_id, 2, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_score__invalid_workout_id(app, workout_id):
    """Test add() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _score = Score(None, 1, workout_id, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_add_score__not_found_workout_id(app, workout_id):
    """Test add() from score model with an workout id that does not exist."""
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _score = Score(None, 1,  workout_id, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('score_value'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_score__invalid_value(app, score_value):
    """Test add() from score model with invalid score value."""
    with app.app_context():
        with pytest.raises(ScoreInvalidValueError) as e:
            _score = Score(None, 1, 2, score_value, True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score value.'


@pytest.mark.parametrize(('score_rx'), (
    (123), (123.42), (1), (0), ([]), (None),
))
def test_add_score__invalid_rx(app, score_rx):
    """Test add() from score model with invalid score rx."""
    with app.app_context():
        with pytest.raises(ScoreInvalidRxError) as e:
            _score = Score(None, 1, 2, '60', score_rx, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score rx state.'


@pytest.mark.parametrize(('score_note'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_score__invalid_note(app, score_note):
    """Test add() from score model with invalid score note."""
    with app.app_context():
        with pytest.raises(ScoreInvalidNoteError) as e:
            _score = Score(None, 1, 2, '60', True, score_note)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score note.'


@pytest.mark.parametrize(('score_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_add_score__invalid_datetime(app, score_datetime):
    """Test add() from score model with invalid score datetime."""
    with app.app_context():
        with pytest.raises(ScoreInvalidDatetimeError) as e:
            _score = Score(None, 1, 2, '60', True,
                           'test note', score_datetime)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score datetime.'
