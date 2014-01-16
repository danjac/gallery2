from functools import partial

from pyramid.events import BeforeRender, subscriber

from .i18n import _
from .lib import filters

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

    def translate(message, *args, **kwargs):
        return request.localizer.translate(_(message, *args, **kwargs))
    event['_'] = translate

    event['format_date'] = partial(filters.format_date, request)
    event['format_time'] = partial(filters.format_time, request)
    event['format_datetime'] = partial(filters.format_datetime, request)
    event['format_currency'] = partial(filters.format_currency, request)
    event['format_number'] = partial(filters.format_number, request)
    event['format_decimal'] = partial(filters.format_number, request)
    event['jsonify'] = partial(filters.jsonify, request)
    event['image_size'] = partial(filters.image_size, request)

    event['route_url'] = request.route_url
    event['static_url'] = request.static_url
    event['storage_url'] = request.storage.url
    event['has_permission'] = request.has_permission
    event['paginate'] = request.paginate
    event['assets'] = partial(event['webassets'], request)
