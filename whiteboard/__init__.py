import os
import time

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')  # Load config.py in project directory

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

    from .views import auth
    from .views import dashboard
    from .views import user
    from .views import workout
    from .views import score
    from .views import movement
    from .views import equipment
    from .views import tag
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(user.bp)
    app.register_blueprint(workout.bp)
    app.register_blueprint(score.bp)
    app.register_blueprint(movement.bp)
    app.register_blueprint(equipment.bp)
    app.register_blueprint(tag.bp)

    return app
