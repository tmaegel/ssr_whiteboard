from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from ..db import get_db
from .auth import login_required
from .user import (
    get_user_prefs
)

bp = Blueprint('tag', __name__, url_prefix='/tag')


@bp.route('/')
@login_required
def list():
    prefs = get_user_prefs()
    sort_pref = ('ASC' if prefs['sortType'] == 0 else 'DESC')

    db = get_db()
    tags = db.execute(
        'SELECT id, userId, tag'
        ' FROM table_tags'
        ' WHERE (userId = 1 OR userId = ?)'
        ' ORDER BY tag ' + sort_pref,
        (g.user['id'],)
    ).fetchall()
    return render_template(
        'tag/tag.html',
        prefs=prefs,
        tags=tags,
        userId=g.user['id'])


# Add tag
@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        tag_name = request.form['tag'].strip()
        error = None

        # @todo: Regex check
        if not tag_name:
            error = 'Tag is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO table_tags'
                ' (userId, tag)'
                ' VALUES (?, ?)',
                (g.user['id'], tag_name,)
            )
            db.commit()

    return redirect(url_for('tag.list'))


# Update tag
@bp.route('/<int:tag_id>/update', methods=('GET', 'POST'))
@login_required
def update(tag_id):
    if request.method == 'POST':
        tag = get_tag(tag_id, True)
        tag_name = request.form['tag'].strip()
        error = None

        if not tag_name:
            error = 'Tag is required.'
        if tag is None:
            error = 'User or Tag ID is invalid.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE table_tags'
                ' SET tag = ?'
                ' WHERE id = ? AND userId = ?',
                (tag_name, tag_id, g.user['id'],)
            )
            db.commit()

    return redirect(url_for('tag.list'))


# Delete tag
@bp.route('/<int:tag_id>/delete')
@login_required
def delete(tag_id):
    error = None

    if get_tag(tag_id, True) is None:
        error = 'User or Tag ID is invalid.'
    else:
        db = get_db()
        db.execute(
            'DELETE FROM table_tags'
            ' WHERE id = ? AND userId = ?',
            (tag_id, g.user['id'],)
        )
        db.commit()

    if error is not None:
        flash(error)

    return redirect(url_for('tag.list'))


# Get tag by id
def get_tag(tag_id, force_user_id=False):
    db = get_db()
    tag = db.execute(
        'SELECT id, userId, tag'
        ' FROM table_tags WHERE id = ?',
        (tag_id,)
    ).fetchone()

    # @todo Raise custom exception here
    if tag is None:
        return None

    if force_user_id:
        if tag['userId'] != g.user['id']:
            return None
    else:
        if tag['userId'] != 1 and tag['userId'] != g.user['id']:
            return None

    return tag
