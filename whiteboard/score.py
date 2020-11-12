from flask import (
    Blueprint, flash, g, redirect, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db
from whiteboard.utils import (
    is_digit, is_float, is_timestamp, is_datetime, datetime_to_sec
)
from whiteboard.workout import (
    get_workout
)

bp = Blueprint('score', __name__, url_prefix='/workout/<int:workout_id>/score')


# Add workout score
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add(workout_id):
    if request.method == 'POST':
        workout = get_workout(workout_id, True)
        score = request.form['score']
        datetime = request.form['datetime']
        note = request.form['note']
        error = None

        if not score:
            error = 'Score is required.'
        elif not is_digit(score) and not is_float(score) and not is_timestamp(score):
            error = 'Score is invalid.'

        if not datetime:
            error = 'Datetime is required.'
        else:
            timestamp_in_sec = datetime_to_sec(datetime)
            if is_datetime(datetime) is False or timestamp_in_sec == -1:
                error = 'Datetime is invalid.'

        if workout is None:
            error = 'User or Workout ID is invalid.'

        if 'rx' in request.form:
            rx = 1
        else:
            rx = 0

        if error is not None:
            flash(error)
            if workout is None:
                return redirect(url_for('workout.list'))
        else:
            db = get_db()
            db.execute(
                'INSERT INTO table_workout_score(userId, workoutId, score, rx, datetime, note)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], workout_id, score, rx, timestamp_in_sec, note,)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))


# Update workout score
@bp.route('/<int:score_id>/update', methods=('GET', 'POST'))
@login_required
def update(workout_id, score_id):
    if request.method == 'POST':
        workout = get_workout(workout_id, True)
        score = request.form['score']
        datetime = request.form['datetime']
        note = request.form['note']
        error = None

        if not score:
            error = 'Score is required.'
        elif not is_digit(score) and not is_float(score) and not is_timestamp(score):
            error = 'Score is invalid.'

        if not datetime:
            error = 'Datetime is required.'
        else:
            timestamp_in_sec = datetime_to_sec(datetime)
            if is_datetime(datetime) is False or timestamp_in_sec == -1:
                error = 'Datetime is invalid.'

        if workout is None:
            error = 'User or Workout ID is invalid.'
        elif get_score(score_id) is None:
            error = 'User or Score ID is invalid.'

        if 'rx' in request.form:
            rx = 1
        else:
            rx = 0

        if error is not None:
            flash(error)
            if workout is None:
                return redirect(url_for('workout.list'))
        else:
            db = get_db()
            db.execute(
                'UPDATE table_workout_score SET workoutId = ?, score = ?, rx = ?, datetime = ?, note = ?'
                ' WHERE id = ? AND userId = ?',
                (workout_id, score, rx, timestamp_in_sec, note, score_id, g.user['id'],)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))


# Delete workout scoree
@bp.route('/<int:score_id>/delete')
@login_required
def delete(workout_id, score_id):
    workout = get_workout(workout_id)
    error = None

    if workout is None:
        error = 'User or Workout ID is invalid.'
    elif get_score(score_id) is None:
        error = 'User or Score ID is invalid.'
    else:
        db = get_db()
        db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE id = ? AND userId = ?',
            (score_id, g.user['id'],)
        )
        db.commit()

    if error is not None:
        flash(error)
        if workout is None:
            return redirect(url_for('workout.list'))

    return redirect(url_for('workout.info', workout_id=workout_id))


def get_score(score_id):
    score = get_db().execute(
        'SELECT id, userId, workoutId, score, rx, datetime, note'
        ' FROM table_workout_score WHERE id = ?',
        (score_id,)
    ).fetchone()

    # @todo Raise custom exception here
    if score is None:
        return None
    if score['userId'] != g.user['id']:
        return None

    return score
