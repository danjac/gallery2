import mock

from pyramid import testing

from ..lib.testing import make_request


def test_home(db):
    from ..views import home
    assert 'images' in home(make_request())


def test_home_functional(app, db):
    res = app.get("/")
    assert res.status_int == 200


def test_logout():
    from ..views.auth import logout
    res = logout(make_request())
    assert res.route_name == 'home'


def test_login_get():
    from ..views.auth import login
    with testing.testConfig() as config:
        config.add_route("login", "/login")
        assert 'form' in login(make_request(route_name='login'))


def test_login_post_invalid(db):
    from ..views.auth import login
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
    from ..views.auth import login
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
    from ..views.auth import signup
    with testing.testConfig() as config:
        config.add_route('signup', '/signup')
        assert 'form' in signup(make_request(route_name='signup'))


def test_signup_post(db):
    from ..models import User
    from ..views.auth import signup
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


def test_signup_functional(app, db):
    from ..models import User

    res = app.get("/signup")
    csrf = res.forms[1]['csrf_token'].value

    post_data = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': 'testpass',
        'password_confirm': 'testpass',
        'csrf_token': csrf,
    }

    res = app.post("/signup", post_data)
    assert res.location == 'http://localhost/'
    assert User.query.count() == 1


def test_upload_get(db):
    from ..views import upload
    with testing.testConfig() as config:
        config.add_route('upload', '/upload')
        res = upload(make_request(route_name='upload'))
    assert 'form' in res


def test_upload_post(db):
    from ..views import upload
    from ..models import Image
    from .factories import UserFactory
    post_data = {
        'title': 'test',
        'taglist': 'testing this',
        'image': mock.Mock(filename='test.jpg'),
    }
    req = make_request(method='POST',
                       post_data=post_data,
                       route_name='upload')
    req.user = UserFactory()
    with testing.testConfig() as config:
        config.add_route('home', '/')
        config.add_route('upload', '/upload')
        with mock.patch('PIL.Image'):
            res = upload(req)
    assert res.route_name == 'detail'
    image = Image.query.first()
    assert image.user == req.user
