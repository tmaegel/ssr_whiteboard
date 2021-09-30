# -*- coding: utf-8 -*-
# List with No Login
def test_list_nologin(client):
    response = client.get('/movement/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


# List with User Login
def test_list_userlogin(client, auth):
    auth.login()
    response = client.get('/movement/')
    assert b'Movement 1' in response.data
    assert b'Movement 2' in response.data
    assert b'Movement 3' in response.data
