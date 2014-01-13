import transaction


# User tests


def test_reset_verification_code():
    from ..models import User
    assert User().reset_verification_code not in (None, '')


def test_check_good_password():
    from ..models import User
    u = User(password="testpass")
    assert u.check_password("testpass")


def test_check_bad_password():
    from ..models import User
    u = User(password="testpass")
    assert not u.check_password("TEST")


def test_null_password():
    from ..models import User
    assert not User().check_password("testpass")


def test_active(db):
    from ..models import DBSession, User
    DBSession.add(User(email="test@gmail.com"))
    transaction.commit()
    assert User.query.active().count() == 1


# Image tests


def test_add_tags(db):

    from ..models import Image, Tag, DBSession
    from .factories import UserFactory

    image = Image(
        user=UserFactory(),
        title='test',
        original_filename='test.jpg',
        image='test.jpg',
        thumbnail='test.jpg',
    )
    image.taglist = 'testing Development'
    DBSession.flush()
    assert Tag.query.count() == 2
    assert image.taglist == ['testing', 'Development']
    assert len(image.tags) == 2

    # test uniqueness

    image2 = Image(
        user=image.user,
        title='another test',
        original_filename='test.jpg',
        image='test.jpg',
        thumbnail='test.jpg',
    )
    image2.taglist = 'testing again'
    DBSession.flush()
    assert Tag.query.count() == 3
    assert image2.taglist == ['testing', 'again']
    assert len(image2.tags) == 2
