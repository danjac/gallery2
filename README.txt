Sample Pyramid gallery application.

Requirements:
    npm
    Python 2.7
    PostgreSQL

Install:

    1) Create database in pgsql
    2) cd gallery2
    3) development.ini: change sqlalchemy.uri as needed
    4) python setup.py develop (you probably want a virtualenv)
    5) initialize_gallery2_db development.ini
    6) npm -g install coffeescript
    7) pserve development.ini 
    8) open browser at localhost:6543
