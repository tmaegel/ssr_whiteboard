import pytest
from whiteboard.db import get_db


def test_add(client, auth, app):
    auth.login()
    assert client.get('/workout/4/score/add', follow_redirects=True).status_code == 200
    client.post(
        '/workout/4/score/add',
        follow_redirects=True,
        data={'score': '1234567890', 'datetime': '14.02.2009 00:31', 'rx': 1, 'note': 'example note'}
    )

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM table_workout_score').fetchone()[0]
        assert count == 5

    response = client.get('/workout/4')
    assert response.status_code == 200
    assert b'1234567890' in response.data
    assert b'14.02.2009 00:31' in response.data
    assert b'example note' in response.data
    assert b'<span class="badge badge-light badge-pill">Rx</span>' in response.data


@pytest.mark.parametrize(('score', 'datetime', 'rx', 'note', 'message'), (
    ('', '14.02.2009 00:31', 1, 'note', b'Score is required.'),
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
