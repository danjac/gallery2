import datetime

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
from ..lib.pagination import Page


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


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
