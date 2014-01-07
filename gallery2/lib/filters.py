import json
import jinja2

from babel import dates, numbers


@jinja2.contextfilter
def format_date(context, value, format='medium'):
    return dates.format_date(value, format, 
                             locale=context['request'].locale)


@jinja2.contextfilter
def format_time(context, value, format='medium'):
    return dates.format_time(value, format, 
                             locale=context['request'].locale)


@jinja2.contextfilter
def format_datetime(context, value, format='medium'):
    return dates.format_datetime(value, format, 
                                 locale=context['request'].locale)


@jinja2.contextfilter
def format_currency(context, value, currency):
    return numbers.format_currency(
        value, currency, locale=context['request'].locale)


@jinja2.contextfilter
def format_number(context, value):
    return numbers.format_number(value, locale=context['request'].locale)


@jinja2.contextfilter
def format_decimal(context, value, format=None):
    return numbers.format_decimal(value, format=None, 
                                  locale=context['request'].locale)


@jinja2.contextfilter
def jsonify(context, value):
    if hasattr(value, '__json__'):
        value = value.__json__(context['request'])
    return jinja2.Markup(json.dumps(value))
