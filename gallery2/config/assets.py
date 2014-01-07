import pyramid_jinja2

from webassets import Bundle


"""
js = Bundle('js/*.js', 
            filters='uglifyjs',
            output='js/site.min.js')
"""


def includeme(config):
    """
    config.add_webasset('js', js)
    """

    """
    Jinja2 integration

    Usage:

    {% assets "js" %}
    <script type="text/javascript" src="{{ASSET_URL}}"></script>
    {% endassets %}
    """
    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    jinja2_env = pyramid_jinja2.get_jinja2_environment(config)
    jinja2_env.assets_environment = config.get_webassets_env() 
