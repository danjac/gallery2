from ..caching import region


def includeme(config):
    if not region.is_configured:
        region.configure_from_config(config.registry.settings, 'cache.')
