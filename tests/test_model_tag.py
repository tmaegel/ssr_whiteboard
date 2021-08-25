import pytest
from whiteboard.exceptions import (
    UserNotFoundError,
    UserInvalidIdError,
    TagNotFoundError,
    TagNoneObjectError,
    TagInvalidIdError,
    TagInvalidNameError,
)
from whiteboard.models.tag import (
    Tag,
)


#
# Tag.get()
#

@pytest.mark.parametrize(('tag_id'), (
    (1),
))
def test_get_tag__valid(app, tag_id):
    """Test get() from tag model with valid data."""
    with app.app_context():
        tag = Tag.get(tag_id)
        assert tag is not None
        assert tag.id == tag_id
        assert tag.user_id == 1
        assert tag.name == 'Hero'


@pytest.mark.parametrize(('tag_id'), (
    (0),
    (99999),
))
def test_get_tag__not_exist(app, tag_id):
    """Test get() from equipemtn model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(TagNotFoundError) as e:
            tag = Tag.get(tag_id)
            assert tag is None
        assert str(
            e.value) == f'Tag with id {tag_id} does not exist.'


@pytest.mark.parametrize(('tag_id'), (
    ('1'),
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_get_tag__invalid(app, tag_id):
    """Test get() from tag model with invalid data."""
    with app.app_context():
        with pytest.raises(TagInvalidIdError) as e:
            tag = Tag.get(tag_id)
            assert tag is None
        assert str(e.value) == 'Invalid tag id.'

#
# Tag.add()
#


def test_add_tag__valid(app):
    """Test add() from tag model with valid data."""
    tag = Tag(
        None,
        1,
        'tag name'
    )
    with app.app_context():
        tag_id = Tag.add(tag)
        assert tag_id is not None
        assert isinstance(tag_id, int) is True


def test_add_tag__invalid_object(app):
    """Test add() from tag model with invalid object."""
    with app.app_context():
        with pytest.raises(TagNoneObjectError) as e:
            tag_id = Tag.add(None)
            assert tag_id is None
        assert str(e.value) == 'Tag object is None.'


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_add_tag__invalid_user_id(app, user_id):
    """Test add() from tag model with invalid user_id."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            tag_id = Tag.add(tag)
            assert tag_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('tag_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_add_tag__invalid_name(app, tag_name):
    """Test add() from tag model with invalid tag name."""
    tag = Tag(
        None,
        1,
        tag_name
    )
    with app.app_context():
        with pytest.raises(TagInvalidNameError) as e:
            tag_id = Tag.add(tag)
            assert tag_id is None
        assert str(e.value) == 'Invalid tag name.'


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_add_tag__not_exist_user_id(app, user_id):
    """Test add() from tag model with an user id that does not exist."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            tag_id = Tag.add(tag)
            assert tag_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'

#
# Tag.update()
#


def test_update_tag__valid(app):
    """Test update() from tag model with valid data."""
    tag = Tag(
        1,
        1,
        'tag name'
    )
    with app.app_context():
        tag_id = Tag.update(tag)
        assert tag_id is not None
        assert isinstance(tag_id, int) is True


def test_update_tag__invalid_object(app):
    """Test update() from tag model with invalid object."""
    with app.app_context():
        with pytest.raises(TagNoneObjectError) as e:
            tag_id = Tag.update(None)
            assert tag_id is None
        assert str(e.value) == 'Tag object is None.'


@pytest.mark.parametrize(('tag_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_tag__invalid_id(app, tag_id):
    """Test update() from tag model with invalidtag id."""
    tag = Tag(
        tag_id,
        1,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(TagInvalidIdError) as e:
            tag_id = Tag.update(tag)
            assert tag_id is None
        assert str(e.value) == 'Invalid tag id.'


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_update_tag__invalid_user_id(app, user_id):
    """Test update() from tag model with invalid user_id."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            tag_id = Tag.update(tag)
            assert tag_id is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('tag_name'), (
    (123),
    (123.42),
    (True),
    ([]),
    (None),
))
def test_update_tag__invalid_name(app, tag_name):
    """Test update() from tag model with invalid tag name."""
    tag = Tag(
        None,
        1,
        tag_name
    )
    with app.app_context():
        with pytest.raises(TagInvalidNameError) as e:
            tag_id = Tag.update(tag)
            assert tag_id is None
        assert str(e.value) == 'Invalid tag name.'


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_update_tag__not_exist_user_id(app, user_id):
    """Test update() from tag model with an user id that does not exist."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            tag_id = Tag.update(tag)
            assert tag_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'

#
# Tag.remove()
#


def test_remove_tag__valid(app):
    """Test remove() from tag model with valid data."""
    tag = Tag(
        1,
        1,
        'tag name'
    )
    with app.app_context():
        result = Tag.remove(tag)
        assert result is True


def test_remove_tag__invalid_object(app):
    """Test remove() from tag model with invalid object."""
    with app.app_context():
        with pytest.raises(TagNoneObjectError) as e:
            result = Tag.remove(None)
            assert result is None
        assert str(e.value) == 'Tag object is None.'


@pytest.mark.parametrize(('tag_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_tag__invalid_id(app, tag_id):
    """Test remove() from tag model with invalid tag id."""
    tag = Tag(
        tag_id,
        1,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(TagInvalidIdError) as e:
            result = Tag.remove(tag)
            assert result is None
        assert str(e.value) == 'Invalid tag id.'


@pytest.mark.parametrize(('user_id'), (
    (-1),
    (1.0),
    ('1.0'),
    (None),
    ('abc'),
    (True),
))
def test_remove_tag__invalid_user_id(app, user_id):
    """Test remove() from tag model with invalid user_id."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserInvalidIdError) as e:
            result = Tag.remove(tag)
            assert result is None
        assert str(e.value) == 'Invalid user id.'


@pytest.mark.parametrize(('user_id'), (
    (0),
    (99999),
))
def test_remove_tag__not_exist_user_id(app, user_id):
    """Test remove() from tag model with an user id that does not exist."""
    tag = Tag(
        None,
        user_id,
        'tag name'
    )
    with app.app_context():
        with pytest.raises(UserNotFoundError) as e:
            tag_id = Tag.remove(tag)
            assert tag_id is None
        assert str(
            e.value) == f'User with id or name {user_id} does not exist.'
