from pyramid.events import BeforeRender, subscriber

from webhelpers2.html import tags


@subscriber(BeforeRender)
def add_renderer_globals(event):
    request = event['request']
    event['h'] = tags
    event['SITE_NAME'] = request.registry.settings.get(
        'gallery2.site_name', 'gallery2'
    )
    event['login_url'] = request.route_url(
        'login',
        _query={'redirect': request.current_route_url()},
    )
