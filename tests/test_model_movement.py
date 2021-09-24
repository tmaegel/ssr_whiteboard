from whiteboard.exceptions import MovementInvalidIdError, MovementNotFoundError
from whiteboard.models.movement import Movement

import pytest


@pytest.mark.parametrize(('movement_id'), (
    (1), ('1'), (1.0),
))
def test_get_movement__valid(app, movement_id):
    """Test get() from movement model with valid data."""
    with app.app_context():
        _movement = Movement(movement_id, None, None)
        movement = _movement.get()
        assert movement is not None
        assert movement.movement_id == int(movement_id)
        assert movement.name == f'Movement {int(movement_id)}'


@pytest.mark.parametrize(('movement_id'), (
    (0), (99999),
))
def test_get_movement__not_found_movement_id(app, movement_id):
    """Test get() from equipemtn model with an id that does not exist."""
    with app.app_context():
        _movement = Movement(movement_id, None, None)
        with pytest.raises(MovementNotFoundError) as e:
            movement = _movement.get()
            assert movement is None
        assert str(
            e.value) == f'Movement with id {movement_id} does not exist.'


@pytest.mark.parametrize(('movement_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_movement__invalid_movement_id(app, movement_id):
    """Test get() from movement model with invalid data."""
    with app.app_context():
        _movement = Movement(movement_id, None, None)
        with pytest.raises(MovementInvalidIdError) as e:
            movement = _movement.get()
            assert movement is None
        assert str(e.value) == 'Invalid movement id.'
