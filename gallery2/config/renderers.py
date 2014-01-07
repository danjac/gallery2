from webhelpers2.text import plural

from ..lib import filters


def includeme(config):
    # if variable is None print '' instead of 'None'
    def _silent_none(value):
        if value is None:
            return ''
        return value

    env = config.get_jinja2_environment()
    env.finalize = _silent_none

    env.filters['plural'] = plural
    env.filters['jsonify'] = filters.jsonify
    env.filters['format_date'] = filters.format_date
    env.filters['format_time'] = filters.format_time
    env.filters['format_datetime'] = filters.format_datetime
    env.filters['format_currency'] = filters.format_currency
    env.filters['format_decimal'] = filters.format_decimal
    env.filters['format_number'] = filters.format_number

