from ..lib.routes import (
    add_model_route,
    route_defaults,
    model_route_defaults,
    seeother,
)

from .. import models


def add_routes(config):

    config.add_route('home', '/')
    config.add_route('search', '/search')
    config.add_route('tags', '/tags')
    config.add_route('upload', '/upload')

    # Auth routes

    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('signup', '/signup')
    config.add_route('forgotpass', '/forgotpass')
    config.add_route('changepass', '/changepass')

    config.add_model_route(models.User, 'profile', '/profile/{id}/{slug}')

    with config.model_route_defaults(models.Image) as r:
        r('detail', '/images/{id}')
        r('edit', '/images/{id}/edit')
        r('delete', '/images/{id}/delete')
        r('add_comment', '/images/{id}/add_comment')

    config.add_model_route(models.Comment,
                           'delete_comment',
                           '/comments/{id}/delete')


def includeme(config):

    config.add_request_method(seeother, 'seeother')

    config.add_directive('add_model_route', add_model_route)
    config.add_directive('route_defaults', route_defaults)
    config.add_directive('model_route_defaults', model_route_defaults)

    add_routes(config)
