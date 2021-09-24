from whiteboard.exceptions import (
    TagInvalidIdError,
    TagInvalidNameError,
    TagNotFoundError,
    UserInvalidIdError,
    UserNotFoundError,
)
from whiteboard.models.tag import Tag

import pytest


@pytest.mark.parametrize(('tag_id'), (
    (1), (1.0), ('1'),
))
def test_update_tag__valid_tag_id(app, tag_id):
    """Test update() from tag model with valid data."""
    with app.app_context():
        _tag = Tag(tag_id, 1, 'tag name')
        result = _tag.update()
        assert result is True


@pytest.mark.parametrize(('user_id'), (
    (1), (1.0), ('1'),
))
def test_update_tag__valid_user_id(app, user_id):
    """Test update() from tag model with valid data."""
    with app.app_context():
        _tag = Tag(1, user_id, 'tag name')
        result = _tag.update()
        assert result is True


@pytest.mark.parametrize(('tag_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_tag__invalid_tag_id(app, tag_id):
    """Test update() from tag model with invalid tag id."""
    with app.app_context():
        with pytest.raises(TagInvalidIdError) as e:
            _tag = Tag(tag_id, 1, 'tag name')
            result = _tag.update()
            assert result is None
        assert str(e.value) == 'Invalid tag id.'


@pytest.mark.parametrize(('tag_id'), (
    (0), (99999),
))
def test_update_tag__not_exist_tag_id(app, tag_id):
    """Test update() from tag model with an tag id that does not exist."""
    with app.app_context():
        with pytest.raises(TagNotFoundError) as e:
            _tag = Tag(tag_id, 1, 'tag name')
            result = _tag.update()
            assert result is None
        assert str(
            e.value) == f'Tag with id {tag_id} does not exist.'


@pytest.mark.parametrize(('user_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_update_tag__invalid_user_id(app, user_id):
    """Test update() from tag model with invalid user_id."""
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            _tag = Tag(1, user_id, 'tag name')
            result = _tag.update()
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0), (99999),
))
def test_update_tag__not_exist_user_id(app, user_id):
    """Test update() from tag model with an user id that does not exist."""
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            _tag = Tag(1, user_id, 'tag name')
            result = _tag.update()
            assert result is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'


@pytest.mark.parametrize(('tag_name'), (
    (123), (123.42), (True), ([]), (None),
))
def test_update_tag__invalid_name(app, tag_name):
    """Test update() from tag model with invalid tag name."""
    with app.app_context():
        with pytest.raises(TagInvalidNameError) as e:
            _tag = Tag(1, 1, tag_name)
            result = _tag.update()
            assert result is None
        assert str(e.value) == 'Invalid tag name.'
