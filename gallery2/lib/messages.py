import functools


class Messages(object):
    """More convenient way of doing localized flash messages"""

    def __init__(self, request):
        self.request = request
        self.success = functools.partial(self.flash, queue='success')
        self.info = functools.partial(self.flash, queue='info')
        self.warning = functools.partial(self.flash, queue='warning')
        self.danger = functools.partial(self.flash, queue='danger')

    def flash(self, message, queue=''):
        message = self.request.localizer.translate(message)
        return self.request.session.flash(message, queue)
