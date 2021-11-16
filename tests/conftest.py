# -*- coding: utf-8 -*-
from whiteboard import create_app
from whiteboard.db import get_db, init_db

import json
import os
import pytest
import tempfile

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
def user_id_admin():
    return 1


@pytest.fixture()
def user_id_user():
    return 2


@pytest.fixture()
def workout_id_admin():
    return 1


@pytest.fixture()
def workout_id_user():
    return 3


@pytest.fixture
def authenticate(client):
    def _wrapper(auth_data):
        return client.post(
            '/rest/v1/auth/login',
            headers={'content-type': 'application/json'},
            data=json.dumps(auth_data))
    return _wrapper


@pytest.fixture()
def auth_admin(authenticate):
    return authenticate({'username': 'admin', 'password': 'secret'})


@pytest.fixture()
def auth_user(authenticate):
    return authenticate({'username': 'test1', 'password': 'secret'})


@pytest.fixture()
def auth_admin_token(auth_admin):
    return json.loads(auth_user.data.decode('utf-8'))['token']


@pytest.fixture()
def auth_user_token(auth_user):
    return json.loads(auth_user.data.decode('utf-8'))['token']


@pytest.fixture()
def workout_get(client, auth_user_token):
    def _wrapper(workout_id):
        return client.get(
            f'/rest/v1/workout/{workout_id}',
            headers={'Authorization': f'Bearer {auth_user_token}'})
    return _wrapper


@pytest.fixture()
def workout_get_no_auth(client):
    def _wrapper(workout_id):
        return client.get(f'/rest/v1/workout/{workout_id}')
    return _wrapper


@pytest.fixture()
def workout_list_get(client, auth_user_token):
    return client.get(
        '/rest/v1/workout',
        headers={'Authorization': f'Bearer {auth_user_token}'})


@pytest.fixture()
def workout_list_get_no_auth(client):
    return client.get('/rest/v1/workout')


@pytest.fixture()
def workout_post(client, auth_user_token):
    def _wrapper(workout_data):
        return client.post('/rest/v1/workout',
                           headers={
                               'content-type': 'application/json',
                               'Authorization': f'Bearer {auth_user_token}'
                           },
                           data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_post_no_auth(client):
    def _wrapper(workout_data):
        return client.post('/rest/v1/workout',
                           headers={'content-type': 'application/json'},
                           data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_put(client, auth_user_token):
    def _wrapper(workout_id, workout_data):
        return client.put(f'/rest/v1/workout/{workout_id}',
                          headers={
                              'content-type': 'application/json',
                              'Authorization': f'Bearer {auth_user_token}'
                          },
                          data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_put_no_auth(client):
    def _wrapper(workout_id, workout_data):
        return client.put(f'/rest/v1/workout/{workout_id}',
                          headers={'content-type': 'application/json'},
                          data=json.dumps(workout_data))
    return _wrapper


@pytest.fixture()
def workout_delete(client, auth_user_token):
    def _wrapper(workout_id):
        return client.delete(
            f'/rest/v1/workout/{workout_id}',
            headers={'Authorization': f'Bearer {auth_user_token}'})
    return _wrapper


@pytest.fixture()
def workout_delete_no_auth(client):
    def _wrapper(workout_id):
        return client.delete(f'/rest/v1/workout/{workout_id}')
    return _wrapper
