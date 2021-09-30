# -*- coding: utf-8 -*-
from whiteboard.exceptions import (
    EquipmentInvalidIdError,
    EquipmentNotFoundError,
)
from whiteboard.models.equipment import Equipment

import pytest


@pytest.mark.parametrize(('equipment_id'), (
    (1), ('1'), (1.0),
))
def test_get_equipment__valid(app, equipment_id):
    """Test get() from equipment model with valid data."""
    with app.app_context():
        _equipment = Equipment(equipment_id, None)
        equipment = _equipment.get()
        assert equipment is not None
        assert equipment.equipment_id == int(equipment_id)
        assert equipment.name == f'Equipment {int(equipment_id)}'


@pytest.mark.parametrize(('equipment_id'), (
    (0), (99999),
))
def test_get_equipment__not_found_equipment_id(app, equipment_id):
    """Test get() from equipemtn model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(EquipmentNotFoundError) as e:
            _equipment = Equipment(equipment_id, None)
            equipment = _equipment.get()
            assert equipment is None
        assert str(
            e.value) == f'Equipment with id {equipment_id} does not exist.'


@pytest.mark.parametrize(('equipment_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_equipment__invalid_equipment_id(app, equipment_id):
    """Test get() from equipment model with invalid data."""
    with app.app_context():
        with pytest.raises(EquipmentInvalidIdError) as e:
            _equipment = Equipment(equipment_id, None)
            equipment = _equipment.get()
            assert equipment is None
        assert str(e.value) == 'Invalid equipment id.'
