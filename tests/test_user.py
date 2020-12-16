import pytest
from whiteboard.db import get_db


# Update user prefs with no Login
def test_prefs_update_nologin(client):
    response = client.post(
        '/user/prefs/update/test',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


# Update user prefs with user Login
def test_prefs_update_userlogin(client, auth):
    auth.login()
    response = client.post(
        '/user/prefs/update/xxx/',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Home' in response.data


# Update user prefs with user Login
def test_prefs_update_paths(client, auth):
    auth.login()
    response = client.post(
        '/user/prefs/update/xxx/',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Home' in response.data

    response = client.post(
        '/user/prefs/update/workout/',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Workouts' in response.data

    response = client.post(
        '/user/prefs/update/movement/',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Movements' in response.data

    response = client.post(
        '/user/prefs/update/equipment/',
        follow_redirects=True,
        data={'inputSort': '0', 'inputFilter': '0'}
    )
    assert response.status_code == 200
    assert b'Equipment' in response.data


def test_prefs_update(client, auth, app):
    auth.login()

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_user_prefs').fetchone()[0]
        assert count == 0

    # Initialize entry in table_user_prefs
    response = client.get('/workout/')
    assert response.status_code == 200

    response = client.post(
        '/user/prefs/update/workout/',
        follow_redirects=True,
        data={'inputSort': '1', 'inputFilter': '2'}
    )
    assert response.status_code == 200
    assert b'Workouts' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_user_prefs').fetchone()[0]
        assert count == 1
        result = db.execute('SELECT * FROM table_user_prefs WHERE userId=2').fetchone()
        assert result['userId'] == 2
        assert result['sortType'] == 1
        assert result['filterType'] == 2


@pytest.mark.parametrize(('inputSort', 'inputFilter', 'message'), (
    ('', '2', b'Sort type is required.'),
    ('1', '', b'Filter type is required.'),
    ('-1', '2', b'Sort type is invalid.'),
    ('1', '-1', b'Filter type is invalid.'),
    ('abc', '2', b'Sort type is invalid.'),
    ('1', 'abc', b'Filter type is invalid.'),
    ('1.5', '2', b'Sort type is invalid.'),
    ('1', '1.5', b'Filter type is invalid.'),
))
def test_prefs_update_validate_input(client, auth, inputSort, inputFilter, message):
    auth.login()
    response = client.post(
        '/user/prefs/update/xxx/',
        follow_redirects=True,
        data={'inputSort': inputSort, 'inputFilter': inputFilter}
    )
    assert message in response.data
