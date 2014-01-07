import transaction


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
