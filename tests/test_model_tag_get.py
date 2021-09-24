from whiteboard.exceptions import TagInvalidIdError, TagNotFoundError
from whiteboard.models.tag import Tag

import pytest


@pytest.mark.parametrize(('tag_id'), (
    (1), (1.0), ('1'),
))
def test_get_tag__valid(app, tag_id):
    """Test get() from tag model with valid data."""
    with app.app_context():
        _tag = Tag(tag_id, None, None)
        tag = _tag.get()
        assert tag is not None
        assert tag.tag_id == int(tag_id)
        assert tag.user_id == 1
        assert tag.name == 'Hero'


@pytest.mark.parametrize(('tag_id'), (
    (0), (99999),
))
def test_get_tag__not_found_tag_id(app, tag_id):
    """Test get() from tag model with an id that does not exist."""
    with app.app_context():
        with pytest.raises(TagNotFoundError) as e:
            _tag = Tag(tag_id, None, None)
            tag = _tag.get()
            assert tag is None
        assert str(e.value) == f'Tag with id {tag_id} does not exist.'


@pytest.mark.parametrize(('tag_id'), (
    (-1), ('1.0'), (None), ('abc'), (True), (False),
))
def test_get_tag__invalid(app, tag_id):
    """Test get() from tag model with invalid data."""
    with app.app_context():
        with pytest.raises(TagInvalidIdError) as e:
            _tag = Tag(tag_id, None, None)
            tag = _tag.get()
            assert tag is None
        assert str(e.value) == 'Invalid tag id.'
