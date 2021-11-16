# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('score_id'), (
    (1), ('1'),
))
def test_get_score__valid_score_id(app, score_id):
    """Test get() from score model with valid score_id."""
    with app.app_context():
        _score = Score(score_id=score_id, user_id=2)
        score = _score.get()
        assert score is not None
        assert score.score_id == int(score_id)
        assert score.user_id == 2
        assert score.workout_id == 1
        assert score.value == '80'
        assert score.rx is True
        assert score.note == 'note 1 for workout A from admin'
        assert score.datetime == 1605114000


@pytest.mark.parametrize(('user_id'), (
    (2), ('2'),
))
def test_get_score__valid_user_id(app, user_id):
    """Test get() from score model with valid score_id."""
    with app.app_context():
        _score = Score(score_id=1, user_id=user_id)
        score = _score.get()
        assert score is not None
        assert score.score_id == 1
        assert score.user_id == int(user_id)
        assert score.workout_id == 1
        assert score.value == '80'
        assert score.rx is True
        assert score.note == 'note 1 for workout A from admin'
        assert score.datetime == 1605114000


@pytest.mark.parametrize(('score_id'), (
    (99999),
))
def test_get_score__not_found_score_id(app, score_id):
    """Test get() from score model with score_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(score_id=score_id, user_id=1)
            result = _score.get()
            assert result is None
        assert str(
            e.value) == f'Score with id {score_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_get_score__not_found_user_id(app, user_id):
    """Test get() from score model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(score_id=1, user_id=user_id)
            result = _score.get()
            assert result is None
        assert str(
            e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('score_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_score__invalid_score_id(app, score_id):
    """Test get() from score model with invalid score_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(score_id=score_id, user_id=1)
            score = _score.get()
            assert score is None
        assert str(e.value) == 'Invalid score_id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_score__invalid_user_id(app, user_id):
    """Test get() from score model with invalid user_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(score_id=1, user_id=user_id)
            score = _score.get()
            assert score is None
        assert str(e.value) == 'Invalid user_id.'
