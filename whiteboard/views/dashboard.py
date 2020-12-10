from flask import (
    Blueprint, render_template
)

from .auth import login_required

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('home/dashboard.html')
