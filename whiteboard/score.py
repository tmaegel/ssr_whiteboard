import time


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db
from whiteboard.utils import (
    is_datetime, get_format_timestamp, timestamp_to_sec, datetime_to_sec
)

bp = Blueprint('score', __name__, url_prefix='/workout/<int:workout_id>/score')


@bp.route('/test', methods=('GET', 'POST'))
@login_required
def test(workout_id):
    print("x")
    return redirect(url_for('workout.list'))


# Add workout score
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add(workout_id):
    print(workout_id)
    if request.method == 'POST':
        score = request.form['score']
        datetime = request.form['datetime']
        note = request.form['note']
        error = None

        if not score:
            error = 'Score is required.'
        if not datetime:
            error = 'Datetime is required.'

        if is_datetime(datetime) is False:
            error = 'Datetime is invalid.'

        timestamp_in_sec = datetime_to_sec(datetime)
        if timestamp_in_sec == -1:
            error = 'Could not parse timestamp.'

        if 'rx' in request.form:
            rx = 1
        else:
            rx = 0

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO table_workout_score(userId, workoutId, score, rx, datetime, note)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], workout_id, score, rx, timestamp_in_sec, note,)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))
