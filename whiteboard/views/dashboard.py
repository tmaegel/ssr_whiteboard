# -*- coding: utf-8 -*-
from .auth import login_required
from flask import Blueprint, render_template

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('home/dashboard.html')
