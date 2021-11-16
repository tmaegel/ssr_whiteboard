# -*- coding: utf-8 -*-
import json
import pytest


def test_rest_auth_login__valid_admin(auth_admin):
    response = auth_admin
    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message', 'token'):
        assert attr in json_resp
    assert json_resp['type'] == 'success'
    assert json_resp['message'] == 'Successfully logged in.'


def test_rest_auth_login__valid_user(auth_user):
    response = auth_user
    assert response.status == '200 OK'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message', 'token'):
        assert attr in json_resp
    assert json_resp['type'] == 'success'
    assert json_resp['message'] == 'Successfully logged in.'


@pytest.mark.parametrize(('username'), (
    (None),
))
def test_rest_auth_login__invalid_user(authenticate, username):
    response = authenticate({'username': username, 'password': 'secret'})
    assert response.status == '400 BAD REQUEST'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message'):
        assert attr in json_resp
    assert 'token' not in json_resp
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == 'Invalid user name.'


@pytest.mark.parametrize(('username'), (
    ('Admin'), ('TEST1'), ('test99'),
))
def test_rest_auth_login__not_found_user(authenticate, username):
    response = authenticate({'username': username, 'password': 'secret'})
    assert response.status == '404 NOT FOUND'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message'):
        assert attr in json_resp
    assert 'token' not in json_resp
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == (
        f'User with id or name {username} does not exist.')


def test_rest_auth_login__empty_user(authenticate):
    response = authenticate({'password': 'secret'})
    assert response.status == '400 BAD REQUEST'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message'):
        assert attr in json_resp
    assert 'token' not in json_resp
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == 'Missing arguments in payload.'


@pytest.mark.parametrize(('password'), (
    ('secret1'), ('SECRET'), (None),
))
def test_rest_auth_login__invalid_password(authenticate, password):
    response = authenticate({'username': 'admin', 'password': password})
    assert response.status == '401 UNAUTHORIZED'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message'):
        assert attr in json_resp
    assert 'token' not in json_resp
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == 'Invalid user password.'


def test_rest_auth_login__empty_password(authenticate):
    response = authenticate({'username': 'admin'})
    assert response.status == '400 BAD REQUEST'
    assert response.headers['Content-Type'] == 'application/json'
    json_resp = json.loads(response.data.decode('utf-8'))
    for attr in ('type', 'message'):
        assert attr in json_resp
    assert 'token' not in json_resp
    assert json_resp['type'] == 'error'
    assert json_resp['message'] == 'Missing arguments in payload.'
