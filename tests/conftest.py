import os
import tempfile

import json
import pytest
from whiteboard import create_app
from whiteboard.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()

    # create the app with common test config
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # create the database and load test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test1', password='secret'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def login_admin(self, username='admin', password='secret'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def workout_dict():
    return {
        'user_id': 1,
        'name': 'test workout name',
        'description': 'test workout description',
        'datetime': 0
    }


@pytest.fixture()
def workout_get(client):
    def _wrapper(workout_id):
        return client.get(f'/rest/v1/workout/{workout_id}')
    return _wrapper


@pytest.fixture()
def workout_list_get(client):
    return client.get('/rest/v1/workout')


@pytest.fixture()
def workout_post(client):
    def _wrapper(workout_data):
        return client.post('/rest/v1/workout',
                           headers={'content-type': 'application/json'},
                           data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_put(client):
    def _wrapper(workout_id, workout_data):
        return client.put(f'/rest/v1/workout/{workout_id}',
                          headers={'content-type': 'application/json'},
                          data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_delete(client):
    def _wrapper(workout_id):
        return client.delete(f'/rest/v1/workout/{workout_id}')
    return _wrapper
