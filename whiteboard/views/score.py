# -*- coding: utf-8 -*-
from ..db import get_db
from ..utils import datetime_to_sec, is_datetime, is_float, is_timestamp
from .auth import login_required
from .workout import get_workout
from flask import Blueprint, flash, g, redirect, request, url_for

bp = Blueprint('score', __name__, url_prefix='/workout/<int:workout_id>/score')


# Add workout score
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add(workout_id):
    if request.method == 'POST':
        workout = get_workout(workout_id)
        score_value = request.form['score'].strip()
        score_datetime = request.form['datetime'].strip()
        score_note = request.form['note'].strip()
        error = None

        if not score_value:
            error = 'Score is required.'
        elif (not score_value.isdigit() and not is_float(score_value)
              and not is_timestamp(score_value)):
            error = 'Score is invalid.'

        if not score_datetime:
            error = 'Datetime is required.'
        else:
            timestamp_in_sec = datetime_to_sec(score_datetime)
            if is_datetime(score_datetime) is False or timestamp_in_sec == -1:
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
                'INSERT INTO table_workout_score'
                '(userId, workoutId, score, rx, datetime, note)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (g.user['id'], workout_id, score_value, rx, timestamp_in_sec,
                 score_note,)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))


# Update workout score
@bp.route('/<int:score_id>/update', methods=('GET', 'POST'))
@login_required
def update(workout_id, score_id):
    if request.method == 'POST':
        workout = get_workout(workout_id)
        score_value = request.form['score'].strip()
        score_datetime = request.form['datetime'].strip()
        score_note = request.form['note'].strip()
        error = None

        if not score_value:
            error = 'Score is required.'
        elif (not score_value.isdigit() and not is_float(score_value)
              and not is_timestamp(score_value)):
            error = 'Score is invalid.'

        if not score_datetime:
            error = 'Datetime is required.'
        else:
            timestamp_in_sec = datetime_to_sec(score_datetime)
            if is_datetime(score_datetime) is False or timestamp_in_sec == -1:
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
                'UPDATE table_workout_score'
                ' SET workoutId = ?, score = ?, rx = ?, datetime = ?, note = ?'
                ' WHERE id = ? AND userId = ?',
                (workout_id, score_value, rx, timestamp_in_sec, score_note,
                 score_id, g.user['id'],)
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
