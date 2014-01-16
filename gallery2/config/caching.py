from mako.lookup import TemplateLookup

from ..caching import region


def includeme(config):
    if not region.is_configured:
        region.configure_from_config(config.registry.settings, 'cache.')

    TemplateLookup(
        directories=config.registry.settings['mako.directories'],
        cache_impl="dogpile.cache",
        cache_args={
            'regions': {'default': region},
        }
    )
