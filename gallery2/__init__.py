import os

from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory

ENV_SETTINGS = {
    'GALLERY2_SQLALCHEMY_URL': 'sqlalchemy.url',
    'GALLERY2_SECRET': 'gallery2.secret',
}


def get_environ_settings():
    return dict((v, os.environ[k]) for k, v in ENV_SETTINGS.iteritems()
                if k in os.environ)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings.update(get_environ_settings())
    config = Configurator(settings=settings)
    
    session_factory = SignedCookieSessionFactory(
        settings['gallery2.secret']
    )

    config.set_session_factory(session_factory)

    # Static files 

    config.add_static_view('static', 'static', cache_max_age=3600)

    # Your includes

    config.include('.config.db')
    config.include('.config.auth')
    config.include('.config.routes')
    config.include('.config.renderers')
    config.include('.config.mail')
    config.include('.config.caching')
    config.include('.config.assets')
    config.include('.config.i18n')

    config.scan()

    return config.make_wsgi_app()
