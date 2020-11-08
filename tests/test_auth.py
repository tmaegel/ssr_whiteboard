import pytest
from flask import g, session
from whiteboard.db import get_db


def test_login(client, auth):
    # test that viewing the page renders without template errors
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b"Login" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data

    # test that successful login redirects to the index page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # login request set the user_id in the session
    # check that the user is loaded from the session
    with client:
        client.get('/')
        assert session['user_id'] == 2
        assert g.user['name'] == 'test1'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('wrong_user', 'test', b'Incorrect username.'),
    ('test1', 'wrong_password', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
