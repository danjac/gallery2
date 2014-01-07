from pyramid import testing

from pyramid_mailer.mailer import DummyMailer
from pyramid_storage.testing import DummyFileStorage


from webob.multidict import MultiDict

from ..models import DBSession


class DummyRedirect(object):

    def __init__(self, route_name, *args, **kwargs):
        self.route_name = route_name
        self.args = args
        self.kwargs = kwargs


class DummyRoute(object):

    def __init__(self, name):
        self.name = name


def make_request(method='GET', post_data=None,
                 get_data=None, params=None, session=None,
                 context=None, user=None, with_csrf=True,
                 is_xhr=False, route_name=None):

    req = testing.DummyRequest(method=method)
    req.user = user
    req.is_xhr = is_xhr
    req.POST = MultiDict(post_data or {})
    req.GET = MultiDict(get_data or {})
    req.storage = DummyFileStorage()
    req.seeother = DummyRedirect
    req.mailer = DummyMailer()
    req.matched_route = DummyRoute(route_name)
    req.db = DBSession

    if params is None:
        params = {}
        params.update(req.GET)
        params.update(req.POST)

    req.params = MultiDict(params or {})
    req.context = context

    session = session or {}
    req.session.update(session)

    if req.method == 'POST' and with_csrf:
        req.POST['csrf_token'] = req.session.get_csrf_token()

    return req
