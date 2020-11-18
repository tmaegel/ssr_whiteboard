from flask import (
    Blueprint, flash, g, redirect, request, url_for
)
from markupsafe import escape

from .auth import login_required
from .db import get_db
from .utils import (
    is_digit
)

bp = Blueprint('user', __name__, url_prefix='/user')


# Update user prefs
@bp.route('/prefs/update/<path:route>', methods=('GET', 'POST'))
@login_required
def prefs_update(route):
    if request.method == 'POST':
        sort_type = request.form['inputSort']
        filter_type = request.form['inputFilter']
        error = None

        if not sort_type:
            error = 'Sort type is required.'
        elif not is_digit(sort_type):
            error = 'Sort type is invalid.'
        if not filter_type:
            error = 'Filter type is required.'
        elif not is_digit(filter_type):
            error = 'Filter type is invalid.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE table_user_prefs SET sortType = ?, filterType = ?'
                ' WHERE userId = ?',
                (sort_type, filter_type, g.user['id'],)
            )
            db.commit()

    if 'workout/' in escape(route):
        return redirect(url_for('workout.list'))
    elif 'movement/' in escape(route):
        return redirect(url_for('movement.list'))
    elif 'equipment/' in escape(route):
        return redirect(url_for('equipment.list'))
    else:
        return redirect(url_for('index'))


def get_user_prefs():
    db = get_db()
    prefs = db.execute(
        'SELECT sortType, filterType'
        ' FROM table_user_prefs WHERE userId = ?',
        (g.user['id'],)
    ).fetchone()

    if prefs is None:
        prefs_default = {
            'sortType': 0,
            'filterType': 0
        }
        db.execute(
            'INSERT INTO table_user_prefs(userId, sortType, filterType)'
            ' VALUES (?, ?, ?)',
            (g.user['id'], prefs_default['sortType'],
             prefs_default['filterType'])
        )
        db.commit()
        return prefs_default

    return prefs
