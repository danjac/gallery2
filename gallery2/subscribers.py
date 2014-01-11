from pyramid.events import BeforeRender, subscriber

from webhelpers2.html import tags


@subscriber(BeforeRender)
def add_renderer_globals(event):
    event['h'] = tags
    event['SITE_NAME'] = event['request'].registry.settings.get(
        'gallery2.site_name', 'gallery2'
    )
