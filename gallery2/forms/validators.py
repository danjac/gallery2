from wtforms import ValidationError

from ..i18n import _


class FileRequired(object):

    message = _('File is required')
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message or self.message

    def __call__(self, form, field):
        if not hasattr(field.data, 'file'):
            raise ValidationError(self.message)
