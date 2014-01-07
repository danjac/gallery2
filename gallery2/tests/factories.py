from factory.alchemy import SQLAlchemyModelFactory

from .. import models


class FactoryBase(SQLAlchemyModelFactory):

    FACTORY_SESSION = models.DBSession


class UserFactory(FactoryBase):
    FACTORY_FOR = models.User

    id = 1
    email = "tester@gmail.com"
    password = "test"
    username = "test"
