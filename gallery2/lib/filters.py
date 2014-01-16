import json
import jinja2
import PIL

from babel import dates, numbers


def format_date(request, value, format='medium'):
    return dates.format_date(value, format,
                             locale=request.locale)


def format_time(request, value, format='medium'):
    return dates.format_time(value, format,
                             locale=request.locale)


def format_datetime(request, value, format='medium'):
    return dates.format_datetime(value, format,
                                 locale=request.locale)


def format_currency(request, value, currency):
    return numbers.format_currency(
        value, currency, locale=request.locale)


def format_number(request, value):
    return numbers.format_number(value, locale=request.locale)


def format_decimal(request, value, format=None):
    return numbers.format_decimal(value, format=None,
                                  locale=request.locale)


def jsonify(request, value):
    if hasattr(value, '__json__'):
        value = value.__json__(request)
    return jinja2.Markup(json.dumps(value))


def image_size(request, value):
    image = PIL.Image.open(request.storage.path(value))
    return image.size
