import pytest
from whiteboard.db import get_db


@pytest.mark.parametrize(('score'), (
    (b'999'),
    (b'999.99'),
    (b'2:30'),
    (b'2:30:45'),
))
def test_add(client, auth, app, score):
    auth.login()
    response = client.get('/workout/4/score/add', follow_redirects=True)
    assert response.status_code == 200

    response = client.post(
        '/workout/4/score/add',
        follow_redirects=True,
        data={
                'score': score,
                'datetime': '14.02.2009 00:31',
                'rx': 1,
                'note': 'Add note to Workout B from test1'
            }
    )
    assert response.status_code == 200
    assert score in response.data
    assert b'14.02.2009 00:31' in response.data
    assert b'Add note to Workout B from test1' in response.data
    assert b'<span class="w3-badge w3-small w3-light-gray w3-round-small padding-4-y padding-8-x">Rx</span>' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout_score').fetchone()[0]
        assert count == 6
        result = db.execute('SELECT * FROM table_workout_score WHERE id=6').fetchone()
        assert result['workoutId'] == 4
        assert result['score'] == score.decode("utf-8")
        assert result['datetime'] == 1234567860
        assert result['rx'] == 1
        assert result['note'] == 'Add note to Workout B from test1'


@pytest.mark.parametrize(('score', 'datetime', 'rx', 'note', 'message'), (
    ('', '14.02.2009 00:31', 1, 'note', b'Score is required.'),
    ('abc', '14.02.2009 00:31', 1, 'note', b'Score is invalid.'),
    ('123abc', '14.02.2009 00:31', 1, 'note', b'Score is invalid.'),
    ('1234567890', '', 1, 'note', b'Datetime is required.'),
    ('1234567890', '14.02.2009', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', '14.02.2009 00:', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', 'abc', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', '123', 1, 'note', b'Datetime is invalid.'),
))
def test_add_validate_input(client, auth, score, datetime, rx, note, message):
    auth.login()
    response = client.post(
        '/workout/4/score/add',
        follow_redirects=True,
        data={'score': score, 'datetime': datetime, 'rx': rx, 'note': note}
    )
    assert message in response.data


# Invalid workoutID
@pytest.mark.parametrize(('workoutId'), (
    ('5'),
    ('99'),
))
def test_add_invalid(client, auth, workoutId):
    auth.login()
    response = client.post(
        '/workout/' + workoutId + '/score/add',
        follow_redirects=True,
        data={
                'score': '999',
                'datetime': '14.02.2009 00:31',
                'rx': 1,
                'note': 'Add note to Workout B from test1'
            }
    )
    assert response.status_code == 200
    assert b'User or Workout ID is invalid.' in response.data


@pytest.mark.parametrize(('score'), (
    (b'999'),
    (b'999.99'),
    (b'2:30'),
    (b'2:30:45'),
))
def test_update(client, auth, app, score):
    auth.login()
    response = client.get('/workout/3/score/2/update', follow_redirects=True)
    assert response.status_code == 200
    assert b'100' in response.data
    assert b'11.11.2020 18:00' in response.data
    assert b'note 1 for workout A from test1' in response.data

    response = client.post(
        '/workout/3/score/2/update',
        follow_redirects=True,
        data={
            'score': score,
            'datetime': '14.02.2009 00:31',
            'note': 'Update note to Workout B from test1'
        }
    )
    assert response.status_code == 200
    assert score in response.data
    assert b'14.02.2009 00:31' in response.data
    assert b'Update note to Workout B from test1' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout_score').fetchone()[0]
        assert count == 5
        result = db.execute('SELECT * FROM table_workout_score WHERE workoutId=3').fetchone()
        assert result['id'] == 2
        assert result['workoutId'] == 3
        assert result['score'] == score.decode("utf-8")
        assert result['rx'] == 0
        assert result['datetime'] == 1234567860
        assert result['note'] == 'Update note to Workout B from test1'


@pytest.mark.parametrize(('score', 'datetime', 'rx', 'note', 'message'), (
    ('', '14.02.2009 00:31', 1, 'note', b'Score is required.'),
    ('abc', '14.02.2009 00:31', 1, 'note', b'Score is invalid.'),
    ('123abc', '14.02.2009 00:31', 1, 'note', b'Score is invalid.'),
    ('1234567890', '', 1, 'note', b'Datetime is required.'),
    ('1234567890', '14.02.2009', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', '14.02.2009 00:', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', 'abc', 1, 'note', b'Datetime is invalid.'),
    ('1234567890', '123', 1, 'note', b'Datetime is invalid.'),
))
def test_update_validate_input(client, auth, score, datetime, rx, note, message):
    auth.login()
    response = client.post(
        '/workout/3/score/2/update',
        follow_redirects=True,
        data={'score': score, 'datetime': datetime, 'rx': rx, 'note': note}
    )
    assert message in response.data


# Invalid workoutID
@pytest.mark.parametrize(('workoutId', 'scoreId', 'message'), (
    ('5', '2', b'User or Workout ID is invalid.'),
    ('99', '2', b'User or Workout ID is invalid.'),
    ('4', '5', b'User or Score ID is invalid.'),
    ('4', '99', b'User or Score ID is invalid.'),
))
def test_update_invalid(client, auth, workoutId, scoreId, message):
    auth.login()
    response = client.post(
        '/workout/' + workoutId + '/score/' + scoreId + '/update',
        follow_redirects=True,
        data={
                'score': '999',
                'datetime': '14.02.2009 00:31',
                'rx': 1,
                'note': 'Add note to Workout B from test1'
            }
    )
    assert response.status_code == 200
    assert message in response.data


# Delete Score from and default workout
def test_delete_default(client, auth, app):
    auth.login()
    response = client.get('/workout/1/score/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Score ID is invalid.' not in response.data
    assert b'note 1 for workout A from admin' not in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) from table_workout_score WHERE workoutId=1').fetchone()[0]
        assert count == 1


# Delete Score from and custom workout
def test_delete_custom(client, auth, app):
    auth.login()
    response = client.get('/workout/3/score/2/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'User or Score ID is invalid.' not in response.data
    assert b'note 1 for workout A from test1' not in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) from table_workout_score WHERE workoutId=3').fetchone()[0]
        assert count == 1


# Invalid workoutID
@pytest.mark.parametrize(('workoutId', 'scoreId', 'message'), (
    ('5', '2', b'User or Workout ID is invalid.'),
    ('99', '2', b'User or Workout ID is invalid.'),
    ('4', '5', b'User or Score ID is invalid.'),
    ('4', '99', b'User or Score ID is invalid.'),
))
def test_delete_invalid(client, auth, workoutId, scoreId, message):
    auth.login()
    response = client.get('/workout/' + workoutId + '/score/' + scoreId + '/delete', follow_redirects=True)
    assert response.status_code == 200
    assert message in response.data
