import pytest
from whiteboard.db import get_db

def test_list(client, auth):
    # No Login
    response = client.get('/equipment/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

    # User Login
    auth.login()
    response = client.get('/equipment/')
    assert b'Equipment 1' in response.data
    assert b'Equipment 2' in response.data
    assert b'Equipment 3' in response.data
