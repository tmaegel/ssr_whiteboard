import pytest
from whiteboard.db import get_db


# List with No Login
def test_list_nologin(client):
    response = client.get('/workout/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


# List with Admin Login
def test_list_adminlogin(client, auth):
    auth.login_admin()
    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Workout A from admin' in response.data
    assert b'Workout A description from admin' in response.data
    assert b'onclick="location.href=\'1\'"' in response.data
    assert b'Workout B from admin' in response.data
    assert b'Workout B description from admin' in response.data
    assert b'onclick="location.href=\'2\'"' in response.data
    assert b'Workout A from test1' not in response.data
    assert b'Workout A description from test1' not in response.data
    assert b'onclick="location.href=\'3\'"' not in response.data
    assert b'Workout B from test1' not in response.data
    assert b'Workout B description from test1' not in response.data
    assert b'onclick="location.href=\'4\'"' not in response.data
    assert b'Workout A from test2' not in response.data
    assert b'Workout A description from test2' not in response.data
    assert b'onclick="location.href=\'5\'"' not in response.data
    assert b'Workout B from test2' not in response.data
    assert b'Workout B description from test2' not in response.data
    assert b'onclick="location.href=\'6\'"' not in response.data

    # Check the tags
    assert b'Tag A from admin' in response.data
    assert b'Tag B from admin' in response.data
    assert b'Tag C from admin' not in response.data
    assert b'Tag D from admin' not in response.data
    assert b'Tag E from admin' not in response.data


# List with User Login
def test_list_userlogin(client, auth):
    auth.login()
    response = client.get('/workout/')
    assert b'Workout A from admin' in response.data
    assert b'Workout A description from admin' in response.data
    assert b'onclick="location.href=\'1\'"' in response.data
    assert b'Workout B from admin' in response.data
    assert b'Workout B description from admin' in response.data
    assert b'onclick="location.href=\'2\'"' in response.data
    assert b'Workout A from test1' in response.data
    assert b'Workout A description from test1' in response.data
    assert b'onclick="location.href=\'3\'"' in response.data
    assert b'Workout B from test1' in response.data
    assert b'Workout B description from test1' in response.data
    assert b'onclick="location.href=\'4\'"' in response.data
    assert b'Workout A from test2' not in response.data
    assert b'Workout A description from test2' not in response.data
    assert b'onclick="location.href=\'5\'"' not in response.data
    assert b'Workout B from test2' not in response.data
    assert b'Workout B description from test2' not in response.data
    assert b'onclick="location.href=\'6\'"' not in response.data

    # Check the tags
    assert b'Tag A from admin' in response.data
    assert b'Tag B from admin' in response.data
    assert b'Tag C from admin' in response.data
    assert b'Tag D from admin' in response.data
    assert b'Tag E from admin' not in response.data


# Info with No Login
def test_info_nologin(client, auth):
    response = client.get('/workout/3', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


# Info with User Login and default workout
def test_info_login_default(client, auth):
    auth.login()
    response = client.get('/workout/2')
    assert response.status_code == 200
    assert b'Workout B from admin' in response.data
    assert b'Workout B description from admin' in response.data
    # Check if delete/edit button is hidden when userId = 1
    assert b'id="btn-edit-workout-hide"' in response.data
    assert b'id="btn-delete-workout-hide"' in response.data
    assert b'id="editTagDialog"' not in response.data
    assert b'id="deleteTagDialog"' not in response.data

    # Check if canvas and score ul is hidden if there is no score
    assert b'<canvas' not in response.data
    assert b'<ul' not in response.data

    # Check the tags
    assert b'Tag A from admin' in response.data
    assert b'Tag B from admin' in response.data
    assert b'Tag C from admin' not in response.data
    assert b'Tag D from admin' not in response.data
    assert b'Tag E from admin' not in response.data


# Info with User Login and custom workout
def test_info_login_custom(client, auth):
    auth.login()
    response = client.get('/workout/3')
    assert response.status_code == 200
    assert b'Workout A from test1' in response.data
    assert b'Workout A description from test1' in response.data
    # Check if delete/edit button is not hidden when userId > 1
    assert b'id="btn-edit-workout-hide"' not in response.data
    assert b'id="btn-delete-workout-hide"' not in response.data
    assert b'id="editTagDialog"' not in response.data
    assert b'id="deleteTagDialog"' not in response.data

    # Check if canvas/ul isn't hidden if there is more than 1 score
    assert b'<canvas' in response.data
    assert b'<ul' in response.data

    response = client.get('/workout/4')
    assert response.status_code == 200
    # Check if canvas is hidden if there is only 1 score
    assert b'<canvas' not in response.data
    assert b'<ul' in response.data
    # Check if rx span element is hidden when the score hasn't the rx switch
    assert b'scoreRx' not in response.data

    # Check the tags
    assert b'Tag A from admin' not in response.data
    assert b'Tag B from admin' not in response.data
    assert b'Tag C from admin' in response.data
    assert b'Tag D from admin' in response.data
    assert b'Tag E from admin' not in response.data


# Invalid workoutID
@pytest.mark.parametrize(('workoutId'), (
    ('5'),
    ('99'),
))
def test_info_login_invalid(client, auth, workoutId):
    auth.login()
    response = client.get('/workout/' + workoutId, follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data


def test_add(client, auth, app):
    auth.login()
    response = client.get('/workout/add', follow_redirects=True)
    assert response.status_code == 200

    response = client.post(
        '/workout/add',
        follow_redirects=True,
        data={
            'name': 'Add Workout C from test1',
            'description': 'Update Workout C description from test1'
        }
    )
    assert response.status_code == 200
    assert b'Add Workout C from test1' in response.data
    assert b'Update Workout C description from test1' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 7
        result = db.execute(
            'SELECT * FROM table_workout WHERE id=7').fetchone()
        assert result['name'] == 'Add Workout C from test1'
        assert result['description'] == 'Update Workout C description from test1'
        assert result['datetime'] != 0

    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Add Workout C from test1' in response.data


@pytest.mark.parametrize(('name', 'description', 'message'), (
    ('Add Workout C from test1', '', b'Description is required.'),
    ('', 'Update Workout C description from test1', b'Name is required.'),
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
    response = client.get('/workout/3/update', follow_redirects=True)
    assert response.status_code == 200
    assert b'Workout A from test1' in response.data
    assert b'Workout A description from test1' in response.data

    response = client.post(
        '/workout/3/update',
        follow_redirects=True,
        data={
            'name': 'Update Workout A from test1',
            'description': 'Update Workout A description from test1'
        }
    )
    assert response.status_code == 200
    assert b'Update Workout A from test1' in response.data
    assert b'Update Workout A description from test1' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 6
        result = db.execute(
            'SELECT * FROM table_workout WHERE id=3').fetchone()
        assert result['name'] == 'Update Workout A from test1'
        assert result['description'] == 'Update Workout A description from test1'
        assert result['datetime'] != 0

    response = client.get('/workout/')
    assert response.status_code == 200
    assert b'Update Workout A from test1' in response.data


@pytest.mark.parametrize(('name', 'description', 'message'), (
    ('Update Workout A from test1', '', b'Description is required.'),
    ('', 'Update Workout A description from test1', b'Name is required.'),
))
def test_update_validate_input(client, auth, name, description, message):
    auth.login()
    response = client.post(
        '/workout/3/update',
        follow_redirects=True,
        data={'name': name, 'description': description}
    )
    assert message in response.data


# Invalid workoutID
@pytest.mark.parametrize(('workoutId'), (
    ('5'),
    ('99'),
))
def test_update_invalid(client, auth, workoutId):
    auth.login()
    response = client.post(
        '/workout/' + workoutId + '/update',
        follow_redirects=True,
        data={
            'name': 'Update Workout A from test2',
            'description': 'Update Workout A description from test2'
        }
    )
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.get('/workout/3/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Workout A from test1' not in response.data

    with app.app_context():
        db = get_db()
        count = db.execute(
            'SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 5
        count = db.execute(
            'SELECT COUNT(id) FROM table_workout WHERE id=3').fetchone()[0]
        assert count == 0
        count = db.execute(
            'SELECT COUNT(id) from table_workout_score WHERE workoutId=3'
        ).fetchone()[0]
        assert count == 0


def test_delete_invalid(client, auth, app):
    auth.login()
    response = client.get('/workout/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data
    assert b'Workout A from admin' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute(
            'SELECT COUNT(id) FROM table_workout').fetchone()[0]
        assert count == 6
        count = db.execute(
            'SELECT COUNT(id) FROM table_workout WHERE id=1').fetchone()[0]
        assert count == 1
        count = db.execute(
            'SELECT COUNT(id) from table_workout_score WHERE workoutId=1'
        ).fetchone()[0]
        assert count == 2


def test_delete_notexist(client, auth, app):
    auth.login()
    response = client.get('/workout/99/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data
