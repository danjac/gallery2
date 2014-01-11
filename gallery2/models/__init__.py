import os
import hashlib
import random
import string
import datetime
import StringIO
import PIL

from PIL import ImageOps

try:
    from StringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

from pyramid.security import Allow, Everyone, ALL_PERMISSIONS

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Unicode,
    UnicodeText,
    String,
    Integer,
    Boolean,
)


from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy


from ..lib import crypt
from .base import DBSession, Base, BaseQuery


class UserQuery(BaseQuery):

    def active(self):
        return self.filter_by(is_active=True)

    def admins(self):
        return self.filter_by(is_admin=True)

    def identify(self, identifier):
        return self.filter(
            (User.username == identifier) |
            (User.email == identifier)).first()

    def authenticate(self, identifier, password):
        user = self.active().identify(identifier)
        if user and user.check_password(password):
            return user


class User(Base):

    query = DBSession.query_property(UserQuery)

    __tablename__ = 'users'

    username = Column(Unicode(60), unique=True, index=True)
    email = Column(String(180), unique=True, index=True)
    encrypted_password = Column('password', String(60))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_code = Column(String(60), unique=True, index=True)

    def __str__(self):
        return self.username

    @property
    def __acl__(self):
        return [(Allow, Everyone, "view")]

    @hybrid_property
    def password(self):
        return self.encrypted_password

    @password.setter
    def set_password(self, password):
        self.encrypted_password = crypt.encrypt_password(password)

    def check_password(self, password):
        return crypt.check_password(password, self.password)

    def renew_verification_code(self):
        code = "".join(
            random.sample(
                string.ascii_letters +
                string.digits +
                string.punctuation, 60))
        self.verification_code = hashlib.md5(code).hexdigest()
        return self.verification_code


class Image(Base):

    THUMBNAIL_SIZE = (300, 300)

    __tablename__ = 'images'

    title = Column(Unicode(100), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    original_filename = Column(Unicode(200), nullable=False)
    image = Column(String(200), nullable=False)
    thumbnail = Column(String(200), nullable=False)
    tagstring = Column(UnicodeText)

    user = relationship(User, backref='images')

    tags = relationship(
        'Tag',
        secondary=lambda: tagged_images,
        backref='images'
    )

    tags_proxy = association_proxy(
        'tags', 'name',
        creator=lambda name:
        Tag.query.get_or_new(name)
    )

    def __str__(self):
        return self.title

    @property
    def __acl__(self):
        return [
            (Allow, Everyone, "view"),
            (Allow, "user:%d" % self.user_id, ALL_PERMISSIONS),
        ]

    @declared_attr
    def __mapper_args__(cls):
        return {'order_by': cls.__table__.c.created_at.desc()}

    def store_image(self, filename, file, storage):

        self.original_filename = filename

        today = datetime.date.today()

        date_prefix = os.path.join(
            str(today.year),
            str(today.month),
            str(today.day),
        )

        self.image = storage.save_file(
            file, filename,
            folder=os.path.join('images', date_prefix),
            randomize=True)

        output = StringIO()
        file.seek(0)
        img = PIL.Image.open(file)

        if img.mode not in ('L', 'RGB'):
            img = img.convert('RGB')
        fit = ImageOps.fit(
            img, self.THUMBNAIL_SIZE, PIL.Image.ANTIALIAS)
        fit.save(output, 'JPEG', quality=100)

        self.thumbnail = storage.save_file(
            output, 'output.jpg',
            folder=os.path.join('thumbs', date_prefix),
            randomize=True)

    @hybrid_property
    def taglist(self):
        if not self.tagstring:
            return ''
        return self.tagstring.split()

    @taglist.setter
    def add_tags(self, tagstring):
        self.tagstring = tagstring
        self.tags_proxy.clear()
        names = [n.lower() for n in tagstring.split()]
        for name in names:
            self.tags_proxy.append(name)


class TagQuery(BaseQuery):

    def get_or_new(self, name):
        return self.filter_by(name=name).first() or Tag(name=name)


class Tag(Base):
    __tablename__ = "tags"

    query = DBSession.query_property(TagQuery)

    name = Column(Unicode(200), nullable=False, unique=True)

    def __str__(self):
        return self.name


tagged_images = Table('tagged_images', Base.metadata,
                      Column('image_id', Integer, ForeignKey(Image.id),
                             primary_key=True),
                      Column('tag_id', Integer, ForeignKey(Tag.id),
                             primary_key=True))
