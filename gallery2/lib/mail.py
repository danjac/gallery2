from pyramid.renderers import render

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


def get_rendered_mail(request, subject, recipients, sender=None,
                      context=None, renderer=None, text_renderer=None, 
                      html_renderer=None, 
                      **kwargs):

    context = context or {}

    if renderer:  # base truncated name
        text_renderer = 'emails/%s.text.jinja2' % renderer
        html_renderer = 'emails/%s.html.jinja2' % renderer

    if not text_renderer:
        raise ValueError("text_renderer required")

    message = Message(subject=subject, 
                      recipients=recipients, 
                      sender=sender)
    message.body = render(text_renderer, context, request)

    if html_renderer:
        message.html = render(html_renderer, context, request)

    return message


def send_rendered_mail(request, *args, **kwargs):
    return get_mailer(request).send(get_rendered_mail(request, *args, **kwargs))
