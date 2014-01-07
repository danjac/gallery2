from pyramid.security import Allow, Everyone, Authenticated


class Root(object):
    def __init__(self, request):
        self.request = request
    __acl__ = [(Allow, Everyone, "view"),
               (Allow, Authenticated, "upload")]
