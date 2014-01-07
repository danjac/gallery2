import datetime
import paginate

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    Query,
)

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from zope.sqlalchemy import ZopeTransactionExtension

from ..caching import region


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class SqlAlchemyWrapper(object):
    """Wrapper class to access elements of a collection."""
    def __init__(self, collection):
        self.collection = collection

    def __getitem__(self, range):
        return self.collection[range]

    def __len__(self):
        if isinstance(self.collection, Query):
            return self.collection.count()
        return len(self.collection)


class Page(paginate.Page):
        """A pagination page that deals with SQLAlchemy ORM objects."""

        def __init__(self, request, collection, *args, **kwargs):
            try:
                page_number = int(request.params['page'])
            except (TypeError, KeyError, ValueError):
                page_number = 1

            def url_maker(page):
                params = request.params.copy()
                params['page'] = page
                return request.current_route_url(_query=params)

            self.window_size = kwargs.pop('window_size', 10)

            super(Page, self).__init__(
                collection, page_number,
                *args, wrapper_class=SqlAlchemyWrapper,
                url_maker=url_maker, **kwargs)

            leftmost_page = max((self.page - (self.window_size // 2)),
                                self.first_page or 1)
            rightmost_page = min((self.page + (self.window_size // 2)),
                                 self.last_page or 1)
            self.window = range(leftmost_page, rightmost_page + 1)


class BaseQuery(Query):

    def from_cache(self, key, region=region, **kwargs):
        return region.get_or_create(key, lambda: self.all(), **kwargs)

    def any(self):
        """Wraps EXISTS call"""
        return DBSession.query(self.exists()).scalar()

    def paginate(self, request, **kwargs):
        return Page(request, self, **kwargs)


class BaseModel(object):

    query = DBSession.query_property(BaseQuery)

    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True)

    @declared_attr
    def created_at(self):
        return Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def updated_at(self):
        return Column(DateTime, onupdate=datetime.datetime.utcnow)


Base = declarative_base(cls=BaseModel)
