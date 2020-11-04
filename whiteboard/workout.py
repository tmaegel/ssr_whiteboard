import time


from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db
from whiteboard.utils import (
    is_datetime, get_format_timestamp, timestamp_to_sec
)

bp = Blueprint('workout', __name__, url_prefix='/workout')


# List all workouts
@bp.route('/')
@login_required
def list():
    db = get_db()
    workouts = db.execute(
        'SELECT id, userId, name, description, datetime'
        ' FROM table_workout WHERE (userId = 1 OR userId = ?)'
        ' ORDER BY name ASC',
        (g.user['id'],)
    ).fetchall()
    return render_template('workout/workout.html', workouts=workouts)


# Get workout info
@bp.route('/<int:workout_id>')
@login_required
def info(workout_id):
    error = None
    db = get_db()
    workout = db.execute(
        'SELECT id, userId, name, description, datetime'
        ' FROM table_workout WHERE id = ? AND (userId = 1 OR userId = ?)',
        (workout_id, g.user['id'],)
    ).fetchone()

    if workout is None:
        error = 'Workout ID is invalid.'
    else:
        scores = db.execute(
            'SELECT id, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE workoutId = ? AND (userId = 1 OR userId = ?)'
            ' ORDER BY datetime ASC',
            (workout_id, g.user['id'],)
        ).fetchall()

    if error is not None:
        flash(error)
        return redirect(url_for('workout.list'))
    else:
        return render_template('workout/entry.html', workout=workout, scores=scores,
                               cur_format_time=get_format_timestamp(), get_format_timestamp=get_format_timestamp,
                               timestamp_to_sec=timestamp_to_sec)


# Add new workout
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        error = None

        # @todo: Regex check
        if not name:
            error = 'Title is required.'
        if not description:
            error = 'description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO table_workout(userId, name, description, datetime)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], name, description, time.time(),)
            )
            db.commit()

    return redirect(url_for('workout.list'))


# Update workout
@bp.route('/<int:workout_id>/update', methods=('GET', 'POST'))
@login_required
def update(workout_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        error = None

        if not name:
            error = 'Title is required.'
        if not description:
            error = 'description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE table_workout SET name = ?, description = ?, datetime = ?'
                ' WHERE id = ? AND userId = ?',
                (name, description, int(time.time()), workout_id, g.user['id'],)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))


# Add workout score
@bp.route('/<int:workout_id>/add', methods=('GET', 'POST'))
@login_required
def add_score(workout_id):
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
                (g.user['id'], workout_id, score, rx, datetime, note,)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))
