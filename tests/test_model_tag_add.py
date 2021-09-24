from whiteboard.exceptions import (
    TagInvalidNameError,
    UserInvalidIdError,
    UserNotFoundError,
)
from whiteboard.models.tag import Tag

import pytest


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_add_tag__valid(app, user_id):
    """Test add() from tag model with valid data."""
    with app.app_context():
        _tag = Tag(None, user_id, 'tag name')
        tag_id = _tag.add()
        assert tag_id is not None
        assert isinstance(tag_id, int) is True


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_add_tag__invalid_user_id(app, user_id):
    """Test add() from tag model with invalid user_id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _tag = Tag(None, user_id, 'tag name')
            tag_id = _tag.add()
            assert tag_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_add_tag__not_found_user_id(app, user_id):
    """Test add() from tag model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _tag = Tag(None, user_id, 'tag name')
            tag_id = _tag.add()
            assert tag_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('tag_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_add_tag__invalid_name(app, tag_name):
    """Test add() from tag model with invalid tag name."""
    with app.app_context():
        with pytest.raises(TagInvalidNameError) as e:
            _tag = Tag(None, 1, tag_name)
            tag_id = _tag.add()
            assert tag_id is None
        assert str(e.value) == 'Invalid tag name.'
