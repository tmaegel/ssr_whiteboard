import pytest
from whiteboard.models.workout import (
    Workout,
    WorkoutNotFoundError,
    WorkoutNoneObjectError,
    WorkoutInvalidIdError,
    WorkoutInvalidUserIdError,
    WorkoutInvalidNameError,
    WorkoutInvalidDescriptionError,
    WorkoutInvalidTimestampError,
)

#
# Workout.get()
#


@pytest.mark.parametrize(('workout_id'), (
    (1),
))
def test_get_workout__valid(app, workout_id):
    """Test get() from workout model with valid data."""
    with app.app_context():
        workout = Workout.get(workout_id)
        assert workout is not None
        assert workout.id == 1
        assert workout.user_id == 1
        assert workout.name == 'Workout A from admin'
        assert workout.description == 'Workout A description from admin'
        assert workout.datetime == 0


@pytest.mark.parametrize(('workout_id'), (
    (0),
    (99999),
))
def test_get_workout__not_exist(app, workout_id):
    """Test get() from workout model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(WorkoutNotFoundError):
            workout = Workout.get(workout_id)
            assert workout is None


@pytest.mark.parametrize(('workout_id'), (
    ('1'),
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_get_workout__invalid(app, workout_id):
    """Test get() from workout model with invalid data."""
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError):
            workout = Workout.get(workout_id)
            assert workout is None

#
# Workout.add()
#


def test_add_workout__valid(app):
    """Test add() from workout model with valid data."""
    workout = Workout(
        None,
        1,
        'test name',
        'test description'
    )
    with app.app_context():
        workout_id = Workout.add(workout)
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


def test_add_workout__invalid_object(app):
    """Test add() from workout model with invalid object."""
    with app.app_context():
        with pytest.raises(WorkoutNoneObjectError):
            workout_id = Workout.add(None)
            assert workout_id is None


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_add_workout__invalid_user_id(app, user_id):
    """Test add() from workout model with invalid user_id."""
    workout = Workout(
        None,
        user_id,
        'test name',
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidUserIdError):
            workout_id = Workout.add(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_workout__invalid_name(app, workout_name):
    """Test add() from workout model with invalid workout name."""
    workout = Workout(
        None,
        1,
        workout_name,
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidNameError):
            workout_id = Workout.add(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_description'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_workout__invalid_description(app, workout_description):
    """Test add() from workout model with invalid workout description."""
    workout = Workout(
        None,
        1,
        'test name',
        workout_description
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidDescriptionError):
            workout_id = Workout.add(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_timestamp'), (
    (-1),
    (123.42),
    (True),
    ([]),
    ("abc"),
    ("123"),
    (None),
))
def test_add_workout__invalid_timestamp(app, workout_timestamp):
    """Test add() from workout model with invalid workout timestamp."""
    workout = Workout(
        None,
        1,
        'test name',
        'test description',
        workout_timestamp
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidTimestampError):
            workout_id = Workout.add(workout)
            assert workout_id is None


#
# Workout.update()
#

def test_update_workout__valid(app):
    """Test update() from workout model with valid data."""
    workout = Workout(
        1,
        1,
        'test name',
        'test description'
    )
    with app.app_context():
        workout_id = Workout.update(workout)
        assert workout_id is not None
        assert isinstance(workout_id, int) is True


def test_update_workout__invalid_object(app):
    """Test update() from workout model with invalid object."""
    with app.app_context():
        with pytest.raises(WorkoutNoneObjectError):
            workout_id = Workout.update(None)
            assert workout_id is None


@pytest.mark.parametrize(('workout_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_workout__invalid_id(app, workout_id):
    """Test update() from workout model with invalidworkout id."""
    workout = Workout(
        workout_id,
        1,
        'test name',
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError):
            workout_id = Workout.update(workout)
            assert workout_id is None


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_workout__invalid_user_id(app, user_id):
    """Test update() from workout model with invalid user_id."""
    workout = Workout(
        None,
        user_id,
        'test name',
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidUserIdError):
            workout_id = Workout.update(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_workout__invalid_name(app, workout_name):
    """Test update() from workout model with invalid workout name."""
    workout = Workout(
        None,
        1,
        workout_name,
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidNameError):
            workout_id = Workout.update(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_description'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_workout__invalid_description(app, workout_description):
    """Test update() from workout model with invalid workout description."""
    workout = Workout(
        None,
        1,
        'test name',
        workout_description
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidDescriptionError):
            workout_id = Workout.update(workout)
            assert workout_id is None


@pytest.mark.parametrize(('workout_timestamp'), (
    (-1),
    (123.42),
    (True),
    ([]),
    ("abc"),
    ("123"),
    (None),
))
def test_update_workout__invalid_timestamp(app, workout_timestamp):
    """Test update() from workout model with invalid workout timestamp."""
    workout = Workout(
        None,
        1,
        'test name',
        'test description',
        workout_timestamp
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidTimestampError):
            workout_id = Workout.update(workout)
            assert workout_id is None


#
# Workout.remove()
#

def test_remove_workout__valid(app):
    """Test remove() from workout model with valid data."""
    workout = Workout(
        1,
        1,
        'test name',
        'test description'
    )
    with app.app_context():
        result = Workout.remove(workout)
        assert result is True


def test_remove_workout__invalid_object(app):
    """Test remove() from workout model with invalid object."""
    with app.app_context():
        with pytest.raises(WorkoutNoneObjectError):
            result = Workout.remove(None)
            assert result is None


@pytest.mark.parametrize(('workout_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_workout__invalid_id(app, workout_id):
    """Test remove() from workout model with invalidworkout id."""
    workout = Workout(
        workout_id,
        1,
        'test name',
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidIdError):
            result = Workout.remove(workout)
            assert result is None


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_workout__invalid_user_id(app, user_id):
    """Test remove() from workout model with invalid user_id."""
    workout = Workout(
        None,
        user_id,
        'test name',
        'test description'
    )
    with app.app_context():
        with pytest.raises(WorkoutInvalidUserIdError):
            result = Workout.remove(workout)
            assert result is None