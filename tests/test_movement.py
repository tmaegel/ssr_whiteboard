import pytest
from whiteboard.db import get_db

def test_list(client, auth):
    # No Login
    response = client.get('/movement/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data

    # User Login
    auth.login()
    response = client.get('/movement/')
    assert b'Movement 1' in response.data
    assert b'Movement 2' in response.data
    assert b'Movement 3' in response.data
