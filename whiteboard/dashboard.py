from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from whiteboard.auth import login_required
from whiteboard.db import get_db

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('dashboard.html')
