from sqlalchemy import engine_from_config

from ..models.base import DBSession, Base, Page


def paginate(request, *args, **kwargs):
    return Page(request, *args, **kwargs)


def includeme(config):
    engine = engine_from_config(config.registry.settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config.add_request_method(lambda r: DBSession, 'db', True)
    config.add_request_method(paginate, 'paginate')
