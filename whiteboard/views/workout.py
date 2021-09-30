# -*- coding: utf-8 -*-
from ..db import get_db
from ..utils import get_format_timestamp, timestamp_to_sec
from .auth import login_required
from .user import get_user_prefs
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

import time

bp = Blueprint('workout', __name__, url_prefix='/workout')


# List all workouts
@bp.route('/')
@login_required
def list():
    db = get_db()
    prefs = get_user_prefs()
    sort_pref = ('ASC' if prefs['sortType'] == 0 else 'DESC')

    if prefs['filterType'] == 0:  # No Filter
        where_clause = 'userId = 1 OR userId = ?'
    elif prefs['filterType'] == 1:  # Default only
        where_clause = 'userId = 1'
    elif prefs['filterType'] == 2:  # Custom only
        where_clause = 'userId = ?'
    else:  # Fallback
        where_clause = 'userId = 1 OR userId = ?'

    if '?' in where_clause:
        workouts_res = db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout'
            ' WHERE (' + where_clause + ')'
            ' ORDER BY name ' + sort_pref,
            (g.user['id'],)
        ).fetchall()
    else:
        workouts_res = db.execute(
            'SELECT id, userId, name, description, datetime'
            ' FROM table_workout'
            ' WHERE (' + where_clause + ')'
            ' ORDER BY name ' + sort_pref
        ).fetchall()

    tags = db.execute(
        'SELECT w.id AS workoutId, t.id AS tagId, t.tag'
        ' FROM table_workout w, table_tags t'
        ' INNER JOIN table_workout_tags on table_workout_tags.tagId = t.id'
        ' AND table_workout_tags.workoutId = w.id'
        ' WHERE (w.userId = 1 OR w.userId = ?)',
        (g.user['id'],)
    ).fetchall()

    workouts = link_workouts_to_tags(workouts_res, tags)

    return render_template(
        'workout/workout.html',
        prefs=prefs,
        workouts=workouts,
        userId=g.user['id'])


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
        if workout is None:
            return redirect(url_for('workout.list'))
    else:
        return render_template(
            'workout/entry.html',
            workout=workout,
            scores=scores,
            userId=g.user['id'],
            cur_format_time=get_format_timestamp(),
            get_format_timestamp=get_format_timestamp,
            timestamp_to_sec=timestamp_to_sec)


# Add new workout
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        workout_name = request.form['name'].strip()
        workout_description = request.form['description'].strip()
        error = None

        # @todo: Regex check
        if not workout_name:
            error = 'Name is required.'
        if not workout_description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO table_workout'
                ' (userId, name, description, datetime)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], workout_name, workout_description, time.time(),)
            )
            db.commit()
            inserted_workout = db.execute(
                'SELECT last_insert_rowid()'
                ' FROM table_workout WHERE userId = ? LIMIT 1',
                (g.user['id'],)
            ).fetchone()

            if inserted_workout['last_insert_rowid()']:
                return redirect(url_for(
                    'workout.info',
                    workout_id=inserted_workout['last_insert_rowid()']))

    return redirect(url_for('workout.list'))


# Update workout
@bp.route('/<int:workout_id>/update', methods=('GET', 'POST'))
@login_required
def update(workout_id):
    if request.method == 'POST':
        workout = get_workout(workout_id, True)
        workout_name = request.form['name'].strip()
        workout_description = request.form['description'].strip()
        error = None

        if not workout_name:
            error = 'Name is required.'
        if not workout_description:
            error = 'Description is required.'
        if workout is None:
            error = 'User or Workout ID is invalid.'

        if error is not None:
            flash(error)
            if workout is None:
                return redirect(url_for('workout.list'))
        else:
            db = get_db()
            db.execute(
                'UPDATE table_workout'
                ' SET name = ?, description = ?, datetime = ?'
                ' WHERE id = ? AND userId = ?',
                (workout_name, workout_description, int(time.time()),
                 workout_id, g.user['id'],)
            )
            db.commit()

    return redirect(url_for('workout.info', workout_id=workout_id))


# Delete workout
@bp.route('/<int:workout_id>/delete')
@login_required
def delete(workout_id):
    error = None

    if get_workout(workout_id, True) is None:
        error = 'User or Workout ID is invalid.'
    else:
        db = get_db()
        db.execute(
            'DELETE FROM table_workout'
            ' WHERE id = ? AND userId = ?',
            (workout_id, g.user['id'],)
        )
        db.commit()
        # @todo: use current delete_score function
        db.execute(
            'DELETE FROM table_workout_score'
            ' WHERE workoutId = ? AND userId = ?',
            (workout_id, g.user['id'],)
        )
        db.commit()

    if error is not None:
        flash(error)

    return redirect(url_for('workout.list'))


# Get the workout and tag list from db
def get_workout(workout_id, force_user_id=False):
    db = get_db()
    workout_res = db.execute(
        'SELECT id, userId, name, description, datetime'
        ' FROM table_workout WHERE id = ?',
        (workout_id,)
    ).fetchone()

    # @todo Raise custom exception here
    if workout_res is None:
        return None

    tags = db.execute(
        'SELECT w.id AS workoutId, t.id AS tagId, t.tag'
        ' FROM table_workout w, table_tags t'
        ' INNER JOIN table_workout_tags on table_workout_tags.tagId = t.id'
        ' AND table_workout_tags.workoutId = w.id'
        ' WHERE w.id = ?',
        (workout_id,)
    ).fetchall()

    workout = link_workout_to_tags(workout_res, tags)
    if force_user_id:
        if workout['userId'] != g.user['id']:
            return None
    else:
        if workout['userId'] != 1 and workout['userId'] != g.user['id']:
            return None

    return workout


# Add tags to all  workouts
def link_workouts_to_tags(workouts, tags):
    workouts_res = []
    for workout in workouts:
        workouts_res.append(link_workout_to_tags(workout, tags))

    return workouts_res


# Add tags to the workout entry
def link_workout_to_tags(workout, tags):
    workout_tags = []
    for tag in tags:
        if tag['workoutId'] == workout['id']:
            workout_tags.append(
                {'tagId': tag['tagId'], 'tag': tag['tag']}
            )
    workout_res = dict(workout)
    workout_res['tags'] = workout_tags

    return workout_res
