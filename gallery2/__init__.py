from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

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
