from pyramid.i18n import get_locale_name
from pyramid.events import BeforeRender, subscriber

from babel.core import Locale
from webhelpers2.html import tags


@subscriber(BeforeRender)
def add_renderer_globals(event):
    event['h'] = tags
