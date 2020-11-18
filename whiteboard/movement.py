from flask import (
    Blueprint, render_template
)

from .auth import login_required
from .db import get_db
from .user import (
    get_user_prefs
)

bp = Blueprint('movement', __name__, url_prefix='/movement')


@bp.route('/')
@login_required
def list():
    prefs = get_user_prefs()
    sort_pref = ('ASC' if prefs['sortType'] == 0 else 'DESC')

    db = get_db()
    movements = db.execute(
        'SELECT id, movement, equipmentIds'
        ' FROM table_movements'
        ' ORDER BY movement ' + sort_pref
    ).fetchall()
    return render_template('movement/movement.html', prefs=prefs, movements=movements)
