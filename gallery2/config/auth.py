from pyramid.authorization import ACLAuthorizationPolicy

from ..auth import AuthenticationPolicy, get_user
from ..resources import Root


def includeme(config):

    authn_policy = AuthenticationPolicy(
        config.registry.settings['gallery2.secret'],
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())

    config.add_request_method(get_user, 'user', reify=True)

    config.set_root_factory(Root)
    config.set_default_permission('view')
