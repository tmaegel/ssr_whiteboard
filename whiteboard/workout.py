import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db
from whiteboard.utils import (
    get_format_timestamp, timestamp_to_sec
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
    workout = get_workout(workout_id)

    if workout is None:
        error = 'User or Workout ID is invalid.'
    else:
        scores = get_db().execute(
            'SELECT id, workoutId, score, rx, datetime, note'
            ' FROM table_workout_score WHERE workoutId = ? AND userId = ?'
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
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'

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
            inserted_workout = db.execute(
                'SELECT last_insert_rowid()'
                ' FROM table_workout WHERE userId = ? LIMIT 1',
                (g.user['id'],)
            ).fetchone()

            if inserted_workout['last_insert_rowid()']:
                return redirect(url_for('workout.info', workout_id=inserted_workout['last_insert_rowid()']))

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
            error = 'Name is required.'
        if not description:
            error = 'Description is required.'

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


# Delete workout
@bp.route('/<int:workout_id>/delete')
@login_required
def delete(workout_id):
    workout = get_workout(workout_id, True)
    error = None

    if workout is None:
        error = 'User or Workout ID is invalid.'
    else:
        db = get_db()
        db.execute(
            'DELETE FROM table_workout'
            ' WHERE id = ? AND userId = ?',
            (workout_id, g.user['id'],)
        )
        db.commit()
        db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE workoutId = ? AND userId = ?',
            (workout_id, g.user['id'],)
        )
        db.commit()

    if error is not None:
        flash(error)

    return redirect(url_for('workout.list'))


def get_workout(workout_id, force_user_id=False):
    workout = get_db().execute(
        'SELECT id, userId, name, description, datetime'
        ' FROM table_workout WHERE id = ?',
        (workout_id,)
    ).fetchone()

    # @todo Raise custom exception here
    if workout is None:
        return None
    if force_user_id:
        if workout['userId'] != g.user['id']:
            return None
    else:
        if workout['userId'] != 1 and workout['userId'] != g.user['id']:
            return None

    return workout
