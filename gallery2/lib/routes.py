import contextlib
import functools

from pyramid.httpexceptions import HTTPSeeOther

from .resources import ModelResource


def seeother(request, route_name, *args, **kwargs):
    # grab the headers first
    headers = kwargs.pop('headers', None)
    url = request.route_url(route_name, *args, **kwargs)
    return HTTPSeeOther(location=url, headers=headers)


def add_model_route(config, model, route_name, pattern,
                    traverse='/{id}', factory=None, 
                    pregenerator=None, **kwargs):

    return config.add_route(route_name, pattern,
                            pregenerator=pregenerator or
                            ModelPregenerator(model),
                            factory=factory or ModelResource.for_model(model),
                            traverse=traverse, **kwargs)


@contextlib.contextmanager
def route_defaults(config, **kwargs):
    yield functools.partial(config.add_route, **kwargs)


@contextlib.contextmanager
def model_route_defaults(config, model, traverse='/{id}', **kwargs):
    yield functools.partial(config.add_model_route, model,
                            traverse=traverse, **kwargs)


class ModelPregenerator(object):
    """Allows us to pass a model instance as first arg
    to a route.
    """

    def __init__(self, model, key='id'):
        self.model = model
        self.key = key

    def __call__(self, request, elements, kw):
        if elements:
            first = elements[0]
            if isinstance(first, self.model):
                kw[self.key] = getattr(first, self.key)
            elements = elements[1:]
        return elements, kw
