import sys
import os
import transaction

from pyramid.paster import bootstrap

from .. import models


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> <ID> <folder>\n'
          '(example: "%s development.ini danjac354@gmail.com wallpapers"'
          ')' % (cmd, cmd))
    sys.exit(1)


def handle_file(user, storage, filename):
    if not storage.filename_allowed(filename):
        return
    title, _ = os.path.splitext(os.path.basename(filename))
    file = open(filename, "rb")
    with transaction.manager:
        image = models.Image(user=user, title=title)
        image.store_image(filename, file, storage)
        models.DBSession.add(image)
        print(image.title + " added")


def main(argv=sys.argv):
    if len(argv) != 4:
        usage(argv)
    config_uri, identifier, folder = sys.argv[1:]
    env = bootstrap(config_uri)

    user = models.User.query.identify(identifier)
    if user is None:
        print('No user found for this email address/username')
        sys.exit(1)

    storage = env['request'].storage

    for path, dirs, files in os.walk(folder):
        for filename in files:
            filename = os.path.join(path, filename)
            try:
                handle_file(user, storage, filename)
            except Exception as e:
                print(e)
