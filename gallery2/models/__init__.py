import hashlib
import random
import string
import StringIO
import PIL

from PIL import ImageOps

try:
    from StringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

from pyramid.security import Allow, Everyone, ALL_PERMISSIONS

from sqlalchemy import (
    Column,
    ForeignKey,
    Unicode,
    String,
    Integer,
    Boolean,
)


from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


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

    username = Column(Unicode(60), unique=True)
    email = Column(String(180), unique=True)
    encrypted_password = Column('password', String(60))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __str__(self):
        return self.username

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

    title = Column(Unicode(100), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    original_filename = Column(Unicode(200), nullable=False)
    image = Column(String(200), nullable=False)
    thumbnail = Column(String(200), nullable=False)

    user = relationship(User, backref='images')

    def __str__(self):
        return self.title

    @property
    def __acl__(self):
        return [
            (Allow, Everyone, "view"),
            (Allow, "user:%d" % self.user_id, ALL_PERMISSIONS),
        ]

    def store_image(self, filename, file, storage):
        self.original_filename = filename
        self.image = storage.save_file(
            file, filename,
            folder='images',
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
            folder='thumbs',
            randomize=True)