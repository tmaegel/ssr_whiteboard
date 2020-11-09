import pytest
from whiteboard.db import get_db


def test_list_nologin(client, auth):
    # No Login
    response = client.get('/workout/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_list_adminlogin(client, auth):
    # Admin Login
    auth.login_admin()
    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Workout A from admin' in response.data
    assert b'Workout B from admin' in response.data
    assert b'Workout A from test1' not in response.data
    assert b'Workout B from test1' not in response.data
    assert b'Workout A from test2' not in response.data
    assert b'Workout B from test2' not in response.data


def test_list_userlogin(client, auth):
    # User Login
    auth.login()
    response = client.get('/workout/')
    assert b'Workout A from admin' in response.data
    assert b'Workout B from admin' in response.data
    assert b'Workout A from test1' in response.data
    assert b'Workout B from test1' in response.data
    assert b'Workout A from test2' not in response.data
    assert b'Workout B from test2' not in response.data


def test_info_nologin(client, auth):
    # No Login
    response = client.get('/workout/3', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_info_login(client, auth):
    # User Login
    auth.login()
    response = client.get('/workout/2')
    assert response.status_code == 200
    assert b'Workout B from admin' in response.data
    assert b'Workout B description from admin' in response.data
    # Check if delete/edit button is hidden when userId = 1
    assert b'id="openDelWorkoutDialog"' not in response.data
    assert b'id="openEditWorkoutDialog"' not in response.data
    # Check if canvas and score table is hidden when there is no score available
    assert b'canvas' not in response.data
    assert b'table' not in response.data

    response = client.get('/workout/3')
    assert response.status_code == 200
    assert b'Workout A from test1' in response.data
    assert b'Workout A description from test1' in response.data
    # Check if delete/edit button is bot hidden when userId > 1
    assert b'id="openDelWorkoutDialog"' in response.data
    assert b'id="openEditWorkoutDialog"' in response.data
    # Check if canvas/table is not hidden when there is more than 1 score available
    assert b'canvas' in response.data
    assert b'table' in response.data

    response = client.get('/workout/4')
    assert response.status_code == 200
    # Check if canvas is hidden when there is only 1 score available
    assert b'canvas' not in response.data
    assert b'table' in response.data
    # Check if rx span element is hidden when the score hasn't the rx switch
    assert b'<span class="badge badge-light badge-pill">Rx</span>' not in response.data

    # Test redirection if workoutId is invalid
    response = client.get('/workout/5', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data


def test_add(client, auth, app):
    auth.login()
    assert client.get('/workout/add', follow_redirects=True).status_code == 200
    client.post(
        '/workout/add',
        follow_redirects=True,
        data={'name': 'Workout X', 'description': 'Workout X Description'}
    )

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 7

    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Workout X' in response.data


@pytest.mark.parametrize(('name', 'description', 'message'), (
    ('Workout X', '', b'Description is required.'),
    ('', 'Workout X description', b'Name is required.'),
))
def test_add_validate_input(client, auth, name, description, message):
    auth.login()
    response = client.post(
        '/workout/add',
        follow_redirects=True,
        data={'name': name, 'description': description}
    )
    assert message in response.data


def test_update(client, auth, app):
    auth.login()
    assert client.get('/workout/3/update', follow_redirects=True).status_code == 200
    client.post(
        '/workout/3/update',
        follow_redirects=True,
        data={'name': 'Workout Y', 'description': 'Workout Y Description'}
    )

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 6
        result = db.execute('SELECT name, description FROM table_workout WHERE id=3').fetchone()
        assert result['name'] == 'Workout Y'
        assert result['description'] == 'Workout Y Description'

    response = client.get('/workout/3')
    assert response.status_code == 200
    assert b'Workout Y' in response.data
    assert b'Workout Y Description' in response.data


@pytest.mark.parametrize(('name', 'description', 'message'), (
    ('Workout Y', '', b'Description is required.'),
    ('', 'Workout Y description', b'Name is required.'),
))
def test_update_validate_input(client, auth, name, description, message):
    auth.login()
    response = client.post(
        '/workout/3/update',
        follow_redirects=True,
        data={'name': name, 'description': description}
    )
    assert message in response.data


def test_delete(client, auth, app):
    auth.login()
    assert client.get('/workout/3/delete', follow_redirects=True).status_code == 200

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 5
        count = db.execute('SELECT COUNT(id) FROM table_workout WHERE id=3').fetchone()[0]
        assert count == 0
        count = db.execute('SELECT COUNT(id) from table_workout_score WHERE workoutId=3').fetchone()[0]
        assert count == 0

    response = client.get('/workout/3', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data
    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Workout A from test1' not in response.data


def test_delete_unauthorized(client, auth, app):
    auth.login()
    response = client.get('/workout/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 6
        count = db.execute('SELECT COUNT(id) FROM table_workout WHERE id=1').fetchone()[0]
        assert count == 1
        count = db.execute('SELECT COUNT(id) from table_workout_score WHERE workoutId=1').fetchone()[0]
        assert count == 1

    response = client.get('/workout/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' not in response.data
    assert b'Workout A from admin' in response.data
    assert b'Workout A description from admin' in response.data
    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Workout A from admin' in response.data
