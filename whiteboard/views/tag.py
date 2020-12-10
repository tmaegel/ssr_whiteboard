from flask import (
    Blueprint, render_template
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
        ' ORDER BY tag ' + sort_pref
    ).fetchall()
    return render_template(
        'tag/tag.html',
        prefs=prefs,
        tags=tags)
