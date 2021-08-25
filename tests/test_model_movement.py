import pytest
from whiteboard.exceptions import (
    MovementNotFoundError,
    MovementInvalidIdError,
)
from whiteboard.models.movement import (
    Movement,
)


#
# Movement.get()
#

@pytest.mark.parametrize(('movement_id'), (
    (1),
    (2),
    (3),
))
def test_get_movement__valid(app, movement_id):
    """Test get() from movement model with valid data."""
    with app.app_context():
        movement = Movement.get(movement_id)
        assert movement is not None
        assert movement.id == movement_id
        assert movement.name == f'Movement {movement_id}'


@pytest.mark.parametrize(('movement_id'), (
    (0),
    (99999),
))
def test_get_movement__not_exist(app, movement_id):
    """Test get() from equipemtn model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(MovementNotFoundError) as e:
            movement = Movement.get(movement_id)
            assert movement is None
        assert str(
            e.value) == f'Movement with id {movement_id} does not exist.'


@pytest.mark.parametrize(('movement_id'), (
    ('1'),
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_get_movement__invalid(app, movement_id):
    """Test get() from movement model with invalid data."""
    with app.app_context():
        with pytest.raises(MovementInvalidIdError) as e:
            movement = Movement.get(movement_id)
            assert movement is None
        assert str(e.value) == 'Invalid movement id.'
