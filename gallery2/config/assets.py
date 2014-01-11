import pyramid_jinja2

from webassets import Bundle


js = Bundle('assets/js/*.js',
            filters='uglifyjs',
            output='js/gallery2.min.js')


css = Bundle('assets/css/*.css',
             filters='cssmin',
             output='css/gallery2.min.css')


def includeme(config):
    config.add_webasset('js', js)
    config.add_webasset('css', css)

    config.add_jinja2_extension('webassets.ext.jinja2.AssetsExtension')
    jinja2_env = pyramid_jinja2.get_jinja2_environment(config)
    jinja2_env.assets_environment = config.get_webassets_env()
