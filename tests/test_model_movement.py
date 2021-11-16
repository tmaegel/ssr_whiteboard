# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.movement import Movement

import pytest


@pytest.mark.parametrize(('movement_id'), (
    (1), ('1'),
))
def test_get_movement__valid_movement_id(app, movement_id):
    """Test get() from movement model with valid movement_id."""
    with app.app_context():
        _movement = Movement(movement_id=movement_id)
        movement = _movement.get()
        assert movement is not None
        assert movement.movement_id == int(movement_id)
        assert movement.name == f'Movement {int(movement_id)}'


@pytest.mark.parametrize(('movement_id'), (
    (99999),
))
def test_get_movement__not_found_movement_id(app, movement_id):
    """Test get() from equipemtn model with movement_id that does not exist."""
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _movement = Movement(movement_id=movement_id)
            movement = _movement.get()
            assert movement is None
        assert str(
            e.value) == f'Movement with id {movement_id} does not exist.'


@pytest.mark.parametrize(('movement_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_movement__invalid_movement_id(app, movement_id):
    """Test get() from movement model with invalid movement_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _movement = Movement(movement_id=movement_id)
            movement = _movement.get()
            assert movement is None
        assert str(e.value) == 'Invalid movement_id.'
