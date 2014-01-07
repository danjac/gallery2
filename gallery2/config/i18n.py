from pyramid.i18n import TranslationStringFactory, get_locale_name

from babel.core import Locale

_ = TranslationStringFactory('gallery2')


def get_locale(request):
    return Locale(get_locale_name(request))


def includeme(config):
    config.add_translation_dirs('gallery2:locale')
    config.add_request_method(get_locale, 'locale', True)
    # config.set_local_negotiator(some_callable)