import os
import sys
import transaction

from pyramid.paster import bootstrap

from alembic.config import Config
from alembic import command

from ..models import (
    DBSession,
    User,
    Base,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    env = bootstrap(config_uri)
    Base.metadata.create_all()

    # stamp the database
    alembic_cfg = Config(config_uri)
    command.stamp(alembic_cfg, "head")

    """
    with transaction.manager:
        user = User(
            first_name="",
            last_name="",
            email="",
            password="",
        )
        DBSession.add_all([user])
    """
