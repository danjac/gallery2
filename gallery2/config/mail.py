from pyramid.renderers import render

from pyramid_mailer import get_mailer

from ..lib.mail import get_rendered_mail, send_rendered_mail


def includeme(config):
    config.add_request_method(get_mailer, 'mailer', True)
    config.add_request_method(get_rendered_mail, 'get_rendered_mail')
    config.add_request_method(send_rendered_mail, 'send_rendered_mail')
