# -*- coding: utf-8 -*-
from .views.rest_auth import Login
from .views.rest_workout import WorkoutEnty, WorkoutList
from flask import Flask
from flask_restful import Api

import os
import time


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')  # Load config.py in project directory
    api = Api(app)

    if test_config is None:
        # overload config with instance/config.py
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Set timezone global
    os.environ['TZ'] = app.config['TIMEZONE']
    time.tzset()

    from . import db
    db.init_app(app)

    from .views import (
        auth,
        dashboard,
        equipment,
        movement,
        score,
        tag,
        user,
        workout,
    )
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(user.bp)
    app.register_blueprint(workout.bp)
    app.register_blueprint(score.bp)
    app.register_blueprint(movement.bp)
    app.register_blueprint(equipment.bp)
    app.register_blueprint(tag.bp)

    # rest
    api.add_resource(Login, '/rest/v1/auth/login')
    api.add_resource(WorkoutList, '/rest/v1/workout')
    api.add_resource(WorkoutEnty, '/rest/v1/workout/<int:workout_id>')

    return app
