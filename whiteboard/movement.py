from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db

bp = Blueprint('movement', __name__, url_prefix='/movement')


@bp.route('/')
@login_required
def movement():
    db = get_db()
    movements = db.execute(
        'SELECT id, movement, equipmentIds'
        ' FROM table_movements'
        ' ORDER BY id'
    ).fetchall()
    return render_template('movement/movement.html', movements=movements)
