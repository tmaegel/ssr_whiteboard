import functools

from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from hashlib import sha256
from flask_bcrypt import Bcrypt

from whiteboard.db import get_db

app = Flask(__name__)
bcrypt = Bcrypt(app)
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, name FROM table_users WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, name, password FROM table_users WHERE name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not bcrypt.check_password_hash(user['password'], sha256(password.encode('utf-8')).hexdigest()):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
