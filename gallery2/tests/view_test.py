from pyramid import testing

from ..lib.testing import make_request


def test_home(db):
    from ..views import home
    assert 'images' in home(make_request())


def test_logout():
    from ..views import logout
    res = logout(make_request())
    assert res.route_name == 'home'


def test_login_get():
    from ..views import login
    with testing.testConfig() as config:
        config.add_route("login", "/login")
        assert 'form' in login(make_request(route_name='login'))


def test_login_post_invalid(db):
    from ..views import login
    data = {
        'email': 'test@gmail.com',
        'password': 'test',
    }
    with testing.testConfig() as config:
        config.add_route("login", "/login")
        res = login(make_request(
            'POST',
            post_data=data,
            route_name='login'
        ))
        assert 'form' in res


def test_login_post_valid(db):
    from ..views import login
    from .factories import UserFactory
    UserFactory()
    data = {
        'identifier': 'tester@gmail.com',
        'password': 'test',
    }
    with testing.testConfig() as config:
        config.add_route("login", "/login")
        res = login(make_request(
            'POST',
            post_data=data,
            route_name='login'
        ))
        assert res.route_name == 'home'


def test_signup_get():
    from ..views import signup
    with testing.testConfig() as config:
        config.add_route('signup', '/signup')
        assert 'form' in signup(make_request(route_name='signup'))


def test_signup_post(db):
    from ..models import User
    from ..views import signup
    with testing.testConfig() as config:
        config.add_route('signup', '/signup')
        req = make_request('POST', post_data={
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'testpass',
            'password_confirm': 'testpass',
            }, route_name='signup')
        res = signup(req)
        assert res.route_name == 'home'
        assert User.query.count() == 1
