import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'whiteboard.sqlite'),
    )

    if test_config is None:
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

    from . import db
    db.init_app(app)

    from . import auth
    from . import dashboard
    from . import user
    from . import workout
    from . import score
    from . import movement
    from . import equipment
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(user.bp)
    app.register_blueprint(workout.bp)
    app.register_blueprint(score.bp)
    app.register_blueprint(movement.bp)
    app.register_blueprint(equipment.bp)

    return app
