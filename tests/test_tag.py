import pytest
from whiteboard.db import get_db


# List with No Login
def test_list_nologin(client):
    response = client.get('/tag/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


# List with Admin Login
def test_list_adminlogin(client, auth):
    auth.login_admin()
    response = client.get('/tag/')
    assert response.status_code == 200
    assert b'Tag A from admin' in response.data
    assert b'Tag B from admin' in response.data
    assert b'Tag C from admin' in response.data
    assert b'Tag D from admin' in response.data
    assert b'Tag E from admin' in response.data
    assert b'Tag A from test1' not in response.data
    assert b'Tag B from test1' not in response.data
    assert b'Tag A from test2' not in response.data

    assert b"openDeleteTagDialog('/tag/', 1)" in response.data
    assert b"openDeleteTagDialog('/tag/', 15)" in response.data
    assert b"openDeleteTagDialog('/tag/', 16)" in response.data
    assert b"openDeleteTagDialog('/tag/', 17)" in response.data
    assert b"openDeleteTagDialog('/tag/', 18)" in response.data
    assert b"openDeleteTagDialog('/tag/', 19)" in response.data
    assert b"openDeleteTagDialog('/tag/', 20)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 21)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 22)" not in response.data

    assert b"openEditTagDialog('/tag/', 1, this)" in response.data
    assert b"openEditTagDialog('/tag/', 15, this)" in response.data
    assert b"openEditTagDialog('/tag/', 16, this)" in response.data
    assert b"openEditTagDialog('/tag/', 17, this)" in response.data
    assert b"openEditTagDialog('/tag/', 18, this)" in response.data
    assert b"openEditTagDialog('/tag/', 19, this)" in response.data
    assert b"openEditTagDialog('/tag/', 20, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 21, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 22, this)" not in response.data


# List with User Login
def test_list_userlogin(client, auth):
    auth.login()
    response = client.get('/tag/')
    assert response.status_code == 200
    assert b'Tag A from admin' in response.data
    assert b'Tag B from admin' in response.data
    assert b'Tag C from admin' in response.data
    assert b'Tag D from admin' in response.data
    assert b'Tag E from admin' in response.data
    assert b'Tag A from test1' in response.data
    assert b'Tag B from test1' in response.data
    assert b'Tag A from test2' not in response.data

    assert b"openDeleteTagDialog('/tag/', 1)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 15)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 16)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 17)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 18)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 19)" not in response.data
    assert b"openDeleteTagDialog('/tag/', 20)" in response.data
    assert b"openDeleteTagDialog('/tag/', 21)" in response.data
    assert b"openDeleteTagDialog('/tag/', 22)" not in response.data

    assert b"openEditTagDialog('/tag/', 1, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 15, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 16, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 17, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 18, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 19, this)" not in response.data
    assert b"openEditTagDialog('/tag/', 20, this)" in response.data
    assert b"openEditTagDialog('/tag/', 21, this)" in response.data
    assert b"openEditTagDialog('/tag/', 22, this)" not in response.data


def test_add(client, auth, app):
    auth.login()
    response = client.get('/tag/add', follow_redirects=True)
    assert response.status_code == 200

    response = client.post(
        '/tag/add',
        follow_redirects=True,
        data={'tag': 'Add Tag C from test1'}
    )
    assert response.status_code == 200
    assert b'Add Tag C from test1' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute(
            'SELECT COUNT(id) FROM table_tags WHERE userId=2').fetchone()[0]
        assert count == 3
        result = db.execute('SELECT * FROM table_tags WHERE id=23').fetchone()
        assert result['userId'] == 2
        assert result['tag'] == 'Add Tag C from test1'

    response = client.get('/tag/')
    assert response.status_code == 200
    assert b'Add Tag C from test1' in response.data


@pytest.mark.parametrize(('tag', 'message'), (
    ('', b'Tag is required.'),
))
def test_add_validate_input(client, auth, tag, message):
    auth.login()
    response = client.post(
        '/tag/add',
        follow_redirects=True,
        data={'tag': tag, }
    )
    assert message in response.data


def test_update(client, auth, app):
    auth.login()
    response = client.get('/tag/20/update', follow_redirects=True)
    assert response.status_code == 200

    response = client.post(
        '/tag/20/update',
        follow_redirects=True,
        data={'tag': 'Update Tag C from test1'}
    )
    assert response.status_code == 200
    assert b'Update Tag C from test1' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute(
            'SELECT COUNT(id) FROM table_tags WHERE userId=2').fetchone()[0]
        assert count == 2
        result = db.execute('SELECT * FROM table_tags WHERE id=20').fetchone()
        assert result['userId'] == 2
        assert result['tag'] == 'Update Tag C from test1'

    response = client.get('/tag/')
    assert response.status_code == 200
    assert b'Update Tag C from test1' in response.data


@pytest.mark.parametrize(('tag', 'message'), (
    ('', b'Tag is required.'),
))
def test_update_validate_input(client, auth, tag, message):
    auth.login()
    response = client.post(
        '/tag/20/update',
        follow_redirects=True,
        data={'tag': tag, }
    )
    assert message in response.data


# Invalid tagId
@pytest.mark.parametrize(('tagId'), (
    ('1'),
    ('99'),
))
def test_update_invalid(client, auth, tagId):
    auth.login()
    response = client.post(
        '/tag/' + tagId + '/update',
        follow_redirects=True,
        data={'tag': 'Update tag with invalid id'}
    )
    assert response.status_code == 200
    assert b'User or Tag ID is invalid.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.get('/tag/20/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Tag A from test1' not in response.data

    with app.app_context():
        db = get_db()
        count = db.execute(
            'SELECT COUNT(id) FROM table_tags WHERE userId=2').fetchone()[0]
        assert count == 1
        count = db.execute(
            'SELECT COUNT(id) FROM table_tags WHERE id=20').fetchone()[0]
        assert count == 0


# Invalid tagId
@pytest.mark.parametrize(('tagId'), (
    ('1'),
    ('99'),
))
def test_delete_invalid(client, auth, tagId):
    auth.login()
    response = client.get(
        '/tag/' + tagId + '/delete',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'User or Tag ID is invalid.' in response.data
