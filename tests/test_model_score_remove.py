# -*- coding: utf-8 -*-
from whiteboard.exceptions import (
    ScoreInvalidIdError,
    ScoreNotFoundError,
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidIdError,
    WorkoutNotFoundError,
)
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('score_id'), (
    (1), (1.0), ('1'),
))
def test_remove_score__valid_score_id(app, score_id):
    """Test remove() from score model with valid data."""
    with app.app_context():
        _score = Score(score_id, 1, 2, '60', True, 'test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_remove_score__valid_user_id(app, user_id):
    """Test remove() from score model with valid data."""
    with app.app_context():
        _score = Score(1, user_id, 2, '60', True, 'test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (1), (1.0), ('1'),
))
def test_remove_score__valid_workout_id(app, workout_id):
    """Test remove() from score model with valid data."""
    with app.app_context():
        _score = Score(1, 1, workout_id, '60', True, 'test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('score_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_score_id(app, score_id):
    """Test remove() from score model with invalid id."""
    with app.app_context():
        with pytest.raises(ScoreInvalidIdError) as e:
            _score = Score(score_id, 1, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid score id.'


@pytest.mark.parametrize(('score_id'), (
    (0), (99999),
))
def test_remove_score__not_exist_score_id(app, score_id):
    """Test remove() from score model with an score id that does not exist."""
    with app.app_context():
        with pytest.raises(ScoreNotFoundError) as e:
            _score = Score(score_id, 1, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'Score with id {score_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_user_id(app, user_id):
    """Test remove() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _score = Score(1, user_id, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_remove_score__not_exist_user_id(app, user_id):
    """Test remove() from score model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _score = Score(1, user_id, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_workout_id(app, workout_id):
    """Test remove() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _score = Score(1, 1, workout_id, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (99999),
))
def test_remove_score__not_exist_workout_id(app, workout_id):
    """
    Test remove() from score model with an workout id that does not exist.
    """
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _score = Score(1, 1, workout_id, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'
