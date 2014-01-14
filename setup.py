import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'pyramid_mailer==0.13',
    'pyramid_jinja2',
    'pyramid_exclog',
    'pyramid_webassets',
    'pyramid_storage',
    'pyramid_redis_sessions',
    'cssmin',
    'Pillow',
    'SQLAlchemy',
    'alembic',
    'dogpile.cache',
    'WTForms==2.0dev',
    'schedule',
    'bcrypt',
    'pytest',
    'factory_boy',
    'mock',
    'freezegun',
    'passlib',
    'py-bcrypt',
    'transaction',
    'webhelpers2',
    'paginate',
    'zope.sqlalchemy',
    'waitress',
    'babel',
    'lingua',
    'ipython',
    ]

setup(name='gallery2',
      version='0.0',
      description='gallery2',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='gallery2',
      install_requires=requires,
      dependency_links=[
          "http://github.com/wtforms/wtforms/tarball/master#egg=WTForms-2.0dev",
      ],
      entry_points="""\
      [paste.app_factory]
      main = gallery2:main
      [console_scripts]
      initialize_gallery2_db = gallery2.scripts.initializedb:main
      run_gallery2_crons = gallery2.scripts.crons:main
      import_gallery2_folder = gallery2.scripts.import_folder:main
      """,
      )
