import pytest

from whiteboard.exceptions import (
    ScoreInvalidDatetimeError,
    ScoreInvalidIdError,
    ScoreInvalidNoteError,
    ScoreInvalidRxError,
    ScoreInvalidValueError,
    ScoreNotFoundError,
    UserInvalidIdError,
    UserNotFoundError,
    WorkoutInvalidIdError,
    WorkoutNotFoundError,
)
from whiteboard.models.score import Score

#
# Score.get()
#


@pytest.mark.parametrize(('score_id'), (
    (1),
))
def test_get_score__valid(app, score_id):
    """Test get() from score model with valid data."""
    with app.app_context():
        _score = Score(score_id, None, None, None, None, None, None)
        score = _score.get()
        assert score is not None
        assert score.score_id == score_id
        assert score.user_id == 2
        assert score.workout_id == 1
        assert score.value == '80'
        assert score.rx is True
        assert score.note == 'note 1 for workout A from admin'
        assert score.datetime == 1605114000


@pytest.mark.parametrize(('score_id'), (
    (0),
    (99999),
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
    ('1'),
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_get_score__invalid(app, score_id):
    """Test get() from score model with invalid data."""
    with app.app_context():
        with pytest.raises(ScoreInvalidIdError) as e:
            _score = Score(score_id, None, None, None, None, None, None)
            score = _score.get()
            assert score is None
        assert str(e.value) == 'Invalid score id.'

#
# Score.add()
#


def test_add_score__valid(app):
    """Test add() from score model with valid data."""
    with app.app_context():
        _score = Score(None, 1, 2, '60', True, 'test note')
        score_id = _score.add()
        assert score_id is not None
        assert isinstance(score_id, int) is True


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_add_score__invalid_user_id(app, user_id):
    """Test add() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _score = Score(None, user_id, 2, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('workout_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_add_score__invalid_workout_id(app, workout_id):
    """Test add() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _score = Score(None, 1, workout_id, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('score_value'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
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
    (123),
    (123.42),
    (1),
    (0),
    ([]),
    (None),
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
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_score__invalid_note(app, score_note):
    """Test add() from score model with invalid score note."""
    with app.app_context():
        with pytest.raises(ScoreInvalidNoteError) as e:
            _score = Score(None, 1, 2, '60', True, score_note)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score note.'


@pytest.mark.parametrize(('score_timestamp'), (
    (-1),
    (123.42),
    (True),
    ([]),
    ("abc"),
    ("123"),
    (None),
))
def test_add_score__invalid_timestamp(app, score_timestamp):
    """Test add() from score model with invalid score timestamp."""
    with app.app_context():
        with pytest.raises(ScoreInvalidDatetimeError) as e:
            _score = Score(None, 1, 2, '60', True,
                           'test note', score_timestamp)
            score_id = _score.add()
            assert score_id is None
        assert str(e.value) == 'Invalid score timestamp.'


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_add_score__not_exist_user_id(app, user_id):
    """Test add() from score model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _score = Score(None, user_id, 2, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (0),
    (99999),
))
def test_add_score__not_exist_workout_id(app, workout_id):
    """Test add() from score model with an workout id that does not exist."""
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _score = Score(None, 1,  workout_id, '60', True, 'test note')
            score_id = _score.add()
            assert score_id is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'


#
# Score.update()
#


def test_update_score__valid(app):
    """Test update() from score model with valid data."""
    with app.app_context():
        _score = Score(1, 1, 2, '60', True, 'test note')
        result = _score.update()
        assert result is True


@pytest.mark.parametrize(('score_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_score__invalid_score_id(app, score_id):
    """Test update() from score model with invalid score id."""
    with app.app_context():
        with pytest.raises(ScoreInvalidIdError) as e:
            _score = Score(score_id, 1, 2, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid score id.'


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_score__invalid_user_id(app, user_id):
    """Test update() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _score = Score(1, user_id, 2, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('workout_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_score__invalid_workout_id(app, workout_id):
    """Test update() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _score = Score(1, 1, workout_id, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('score_value'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_score__invalid_value(app, score_value):
    """Test update() from score model with invalid score value."""
    with app.app_context():
        with pytest.raises(ScoreInvalidValueError) as e:
            _score = Score(1, 1, 2, score_value, True, 'test note')
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid score value.'


@pytest.mark.parametrize(('score_rx'), (
    (123),
    (123.42),
    (1),
    (0),
    ([]),
    (None),
))
def test_update_score__invalid_rx(app, score_rx):
    """Test update() from score model with invalid score rx."""
    with app.app_context():
        with pytest.raises(ScoreInvalidRxError) as e:
            _score = Score(1, 1, 2, '60', score_rx, 'test note')
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid score rx state.'


@pytest.mark.parametrize(('score_note'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_score__invalid_note(app, score_note):
    """Test update() from score model with invalid score note."""
    with app.app_context():
        with pytest.raises(ScoreInvalidNoteError) as e:
            _score = Score(1, 1, 2, '60', True, score_note)
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid score note.'


@pytest.mark.parametrize(('score_timestamp'), (
    (-1),
    (123.42),
    (True),
    ([]),
    ("abc"),
    ("123"),
    (None),
))
def test_update_score__invalid_timestamp(app, score_timestamp):
    """Test update() from score model with invalid score timestamp."""
    with app.app_context():
        with pytest.raises(ScoreInvalidDatetimeError) as e:
            _score = Score(1, 1, 2, '60', True, 'test note', score_timestamp)
            result = _score.update()
            assert result is None
        assert str(e.value) == 'Invalid score timestamp.'


@pytest.mark.parametrize(('score_id'), (
    (0),
    (99999),
))
def test_update_score__not_exist_score_id(app, score_id):
    """Test update() from score model with an score id that does not exist."""
    with app.app_context():
        with pytest.raises(ScoreNotFoundError) as e:
            _score = Score(score_id, 1, 2, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(
            e.value) == f'Score with id {score_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_update_score__not_exist_user_id(app, user_id):
    """Test update() from score model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _score = Score(1, user_id, 2, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('workout_id'), (
    (0),
    (99999),
))
def test_update_score__not_exist_workout_id(app, workout_id):
    """
    Test update() from score model with an workout id that does not exist.
    """
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError) as e:
            _score = Score(1, 1, workout_id, '60', True, 'test note')
            result = _score.update()
            assert result is None
        assert str(
            e.value) == f'Workout with id {workout_id} does not exist.'


#
# Score.remove()
#


def test_remove_score__valid(app):
    """Test remove() from score model with valid data."""
    with app.app_context():
        _score = Score(1, 1, 2, '60', True, 'test note')
        result = _score.remove()
        assert result is True


@pytest.mark.parametrize(('score_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_score__invalid_score_id(app, score_id):
    """Test remove() from score model with invalid id."""
    with app.app_context():
        with pytest.raises(ScoreInvalidIdError) as e:
            _score = Score(score_id, 1, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid score id.'


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_score__invalid_user_id(app, user_id):
    """Test remove() from score model with invalid user id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _score = Score(1, user_id, 2, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('workout_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_score__invalid_workout_id(app, workout_id):
    """Test remove() from score model with invalid workout id."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError) as e:
            _score = Score(1, 1, workout_id, '60', True, 'test note')
            result = _score.remove()
            assert result is None
        assert str(e.value) == 'Invalid workout id.'


@pytest.mark.parametrize(('score_id'), (
    (0),
    (99999),
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
    (0),
    (99999),
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
    (0),
    (99999),
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
