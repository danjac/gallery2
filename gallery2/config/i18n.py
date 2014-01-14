from pyramid.i18n import get_locale_name

from babel.core import Locale

from ..lib.messages import Messages


def get_locale(request):
    return Locale(get_locale_name(request))


def includeme(config):
    config.add_translation_dirs('gallery2:locale')
    config.add_request_method(get_locale, 'locale', True)
    config.add_request_method(Messages, 'messages', True)
