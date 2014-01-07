from ..caching import region


def includeme(config):
    region.configure_from_config(config.registry.settings, 'cache.')
