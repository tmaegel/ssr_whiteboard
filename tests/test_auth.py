# -*- coding: utf-8 -*-
from flask import g, session

import pytest


def test_login(client, auth):
    # test that viewing the page renders without template errors
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

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
    ('', 'test', b'Incorrect username.'),
    ('test1', '', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session


def test_passwd_update_nologin(client):
    response = client.post(
        '/auth/passwd/update',
        follow_redirects=True,
        data={'password1': '123456', 'password2': '123456'}
    )
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_passwd_update_userlogin(client, auth):
    auth.login()
    response = client.post(
        '/auth/passwd/update',
        follow_redirects=True,
        data={'password1': '123456', 'password2': '123456'}
    )
    assert response.status_code == 200
    assert b'Home' in response.data

    response = client.post(
        '/auth/login',
        follow_redirects=True,
        data={'username': 'test1', 'password': '123456'}
    )
    assert response.status_code == 200
    assert b'Home' in response.data


@pytest.mark.parametrize(('password1', 'password2', 'message'), (
    ('', '', b'Passwords are not equal.'),
    ('123456', '', b'Passwords are not equal.'),
    ('', '123456', b'Passwords are not equal.'),
    ('123', '456', b'Passwords are not equal.'),
))
def test_passwd_udpate_validate_input(
        client, auth, password1, password2, message):
    auth.login()
    response = client.post(
        '/auth/passwd/update',
        follow_redirects=True,
        data={'password1': password1, 'password2': password2}
    )
    assert message in response.data
