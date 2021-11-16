# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('score_id'), (
    (1), ('1'),
))
def test_remove_score__valid_score_id(app, score_id):
    """Test remove() from score model with valid score_id."""
    with app.app_context():
        _score = Score(score_id=score_id, user_id=1, workout_id=2,
                       value='60', rx=True, note='test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_remove_score__valid_user_id(app, user_id):
    """Test remove() from score model with valid user_id."""
    with app.app_context():
        _score = Score(score_id=1, user_id=user_id, workout_id=2,
                       value='60', rx=True, note='test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('workout_id'), (
    (1), ('1'),
))
def test_remove_score__valid_workout_id(app, workout_id):
    """Test remove() from score model with valid workout_id."""
    with app.app_context():
        _score = Score(score_id=1, user_id=1, workout_id=workout_id,
                       value='60', rx=True, note='test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('score_id'), (
    (99999),
))
def test_remove_score__not_found_score_id(app, score_id):
    """Test remove() from score model with score_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(score_id=score_id, user_id=1, workout_id=2,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'Score with id {score_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_remove_score__not_found_user_id(app, user_id):
    """Test remove() from score model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(score_id=1, user_id=user_id, workout_id=2,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (99999),
))
def test_remove_score__not_found_workout_id(app, workout_id):
    """
    Test remove() from score model with workout_id that does not exist.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(score_id=1, user_id=1, workout_id=workout_id,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('score_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_score_id(app, score_id):
    """Test remove() from score model with invalid score_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(score_id=score_id, user_id=1, workout_id=2,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid score_id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_user_id(app, user_id):
    """Test remove() from score model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(score_id=1, user_id=user_id, workout_id=2,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid user_id.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_remove_score__invalid_workout_id(app, workout_id):
    """Test remove() from score model with invalid workout_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(score_id=1, user_id=1, workout_id=workout_id,
                           value='60', rx=True, note='test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid workout_id.'
