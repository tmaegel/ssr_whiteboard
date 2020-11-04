from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db

bp = Blueprint('equipment', __name__, url_prefix='/equipment')


@bp.route('/')
@login_required
def movement():
    db = get_db()
    equipment = db.execute(
        'SELECT id, equipment'
        ' FROM table_equipment'
        ' ORDER BY id'
    ).fetchall()
    return render_template('equipment/equipment.html', equipment=equipment)
