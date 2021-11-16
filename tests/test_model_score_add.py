# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.score import Score

import pytest


@pytest.mark.parametrize(('user_id'), (
    (1), ('1'),
))
def test_add_score__valid_user_id(app, user_id):
    """Test add() from score model with valid user_id (no datetime)."""
    with app.app_context():
        _score = Score(user_id=user_id, workout_id=2, value='60', rx=True,
                       note='test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('workout_id'), (
    (1), ('1'),
))
def test_add_score__valid_workout_id(app, workout_id):
    """Test add() from score model with valid workout_id (no datetime)."""
    with app.app_context():
        _score = Score(user_id=1, workout_id=workout_id, value='60', rx=True,
                       note='test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('score_datetime'), (
    (123), ('123'),
))
def test_add_score__valid_with_datetime(app, score_datetime):
    """Test add() from score model with valid data (no datetime)."""
    with app.app_context():
        _score = Score(user_id=1, workout_id=2, value='60', rx=True,
                       note='test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('workout_id'), (
    (99999),
))
def test_add_score__not_found_workout_id(app, workout_id):
    """Test add() from score model with workout_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(user_id=1, workout_id=workout_id, value='60',
                           rx=True, note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (99999),
))
def test_add_score__not_found_user_id(app, user_id):
    """Test add() from score model with user_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _score = Score(user_id=user_id, workout_id=1, value='60', rx=True,
                           note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'User with id {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_score__invalid_workout_id(app, workout_id):
    """Test add() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=1, workout_id=workout_id, value='60',
                           rx=True, note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid workout_id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_score__invalid_user_id(app, user_id):
    """Test add() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=user_id, workout_id=1, value='60', rx=True,
                           note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid user_id.'


@pytest.mark.parametrize(('score_value'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_score__invalid_value(app, score_value):
    """Test add() from score model with invalid score value."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=1, workout_id=1, value=score_value, rx=True,
                           note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid value.'


@pytest.mark.parametrize(('score_rx'), (
    (123), (123.42), (1), (0), ([]), (None),
))
def test_add_score__invalid_rx(app, score_rx):
    """Test add() from score model with invalid score rx."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=1, workout_id=1, value='60', rx=score_rx,
                           note='test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid rx.'


@pytest.mark.parametrize(('score_note'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_score__invalid_note(app, score_note):
    """Test add() from score model with invalid score note."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=1, workout_id=1, value='60', rx=True,
                           note=score_note)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid note.'


@pytest.mark.parametrize(('score_datetime'), (
    (-1), (True), ([]), ('abc'), ('123.45'), (123.45), (None),
))
def test_add_score__invalid_datetime(app, score_datetime):
    """Test add() from score model with invalid score datetime."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _score = Score(user_id=1, workout_id=1, value='60', rx=True,
                           note='test note', datetime=score_datetime)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid datetime.'
