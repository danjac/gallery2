from pyramid import testing
from sqlalchemy import create_engine


DB_URI = 'sqlite:///:memory:'


def pytest_funcarg__config(request):

    config = testing.setUp()
    request.addfinalizer(lambda: testing.tearDown())
    return config


def pytest_funcarg__db(request):

    from .. models import DBSession, Base

    engine = create_engine(DB_URI)

    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    request.addfinalizer(lambda: DBSession.remove())

    return engine
