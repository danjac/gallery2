from pyramid.security import (
    Everyone,
    Authenticated,
)

from pyramid.authentication import AuthTktAuthenticationPolicy

from .models import User
from .security import Admins


def get_user(request):

    user_id = request.unauthenticated_userid
    if user_id:
        return User.query.active().filter(User.id == user_id).first()


class AuthenticationPolicy(AuthTktAuthenticationPolicy):

    def effective_principals(self, request):
        rv = [Everyone]
        if request.user:
            rv.append(Authenticated)
            rv.append("user:%d" % request.user.id)
            if request.user.is_admin:
                rv.append(Admins)
        return rv
