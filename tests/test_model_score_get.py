# -*- coding: utf-8 -*-
from whiteboard.exceptions import ScoreInvalidIdError, ScoreNotFoundError
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('score_id'), (
    (1), (1.0), ('1'),
))
def test_get_score__valid(app, score_id):
    """Test get() from score model with valid data."""
    with app.app_context():
        _score = Score(score_id, None, None, None, None, None, None)
        score = _score.get()
        assert score is not None
        assert score.score_id == int(score_id)
        assert score.user_id == 2
        assert score.workout_id == 1
        assert score.value == '80'
        assert score.rx is True
        assert score.note == 'note 1 for workout A from admin'
        assert score.datetime == 1605114000


@pytest.mark.parametrize(('score_id'), (
    (0), (99999),
))
def test_get_score__not_exist_score_id(app, score_id):
    """Test get() from score model with an score id that does not exist."""
    with app.app_context():
        with pytest.raises(ScoreNotFoundError) as e:
            _score = Score(score_id, None, None, None, None, None, None)
            result = _score.get()
            assert result is None
        assert str(
            e.value) == f'Score with id {score_id} does not exist.'


@pytest.mark.parametrize(('score_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_score__invalid(app, score_id):
    """Test get() from score model with invalid data."""
    with app.app_context():
        with pytest.raises(ScoreInvalidIdError) as e:
            _score = Score(score_id, None, None, None, None, None, None)
            score = _score.get()
            assert score is None
        assert str(e.value) == 'Invalid score id.'
