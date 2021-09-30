# -*- coding: utf-8 -*-
from ..db import get_db
from .auth import login_required
from .user import get_user_prefs
from flask import Blueprint, render_template

bp = Blueprint('equipment', __name__, url_prefix='/equipment')


@bp.route('/')
@login_required
def list():
    prefs = get_user_prefs()
    sort_pref = ('ASC' if prefs['sortType'] == 0 else 'DESC')

    db = get_db()
    equipment = db.execute(
        'SELECT id, equipment'
        ' FROM table_equipment'
        ' ORDER BY equipment ' + sort_pref
    ).fetchall()
    return render_template(
        'equipment/equipment.html',
        prefs=prefs,
        equipment=equipment)
