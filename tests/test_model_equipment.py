# -*- coding: utf-8 -*-
from whiteboard.exceptions import InvalidAttributeError, NotFoundError
from whiteboard.models.equipment import Equipment

import pytest


@pytest.mark.parametrize(('equipment_id'), (
    (1), ('1'),
))
def test_get_equipment__valid_equipment_id(app, equipment_id):
    """Test get() from equipment model with valid equipment_id."""
    with app.app_context():
        _equipment = Equipment(equipment_id=equipment_id)
        equipment = _equipment.get()
        assert equipment is not None
        assert equipment.equipment_id == int(equipment_id)
        assert equipment.name == f'Equipment {int(equipment_id)}'


@pytest.mark.parametrize(('equipment_id'), (
    (99999),
))
def test_get_equipment__not_found_equipment_id(app, equipment_id):
    """
    Test get() from equipemtn model with equipment_id that does not exist.
    """
    with app.app_context():
        with pytest.raises(NotFoundError) as e:
            _equipment = Equipment(equipment_id=equipment_id)
            equipment = _equipment.get()
            assert equipment is None
        assert str(
            e.value) == f'Equipment with id {equipment_id} does not exist.'


@pytest.mark.parametrize(('equipment_id'), (
    (0), (-1), (1.0), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_equipment__invalid_equipment_id(app, equipment_id):
    """Test get() from equipment model with invalid equipment_id."""
    with app.app_context():
        with pytest.raises(InvalidAttributeError) as e:
            _equipment = Equipment(equipment_id=equipment_id)
            equipment = _equipment.get()
            assert equipment is None
        assert str(e.value) == 'Invalid equipment_id.'
