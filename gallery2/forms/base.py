from pyramid.i18n import get_locale_name
from webob.multidict import MultiDict

from wtforms import Form as BaseForm
from wtforms.csrf.core import CSRF as BaseCSRF

from ..config.i18n import _


class Form(BaseForm): 
    def __init__(self, request, *args, **kwargs):

        self.request = request
        self.action = kwargs.pop('action', self.request.current_route_url())
        self._obj = kwargs.get('obj')

        params = kwargs.pop('params', self.request.POST)
        locales = [get_locale_name(request)]

        super(Form, self).__init__(
            params, 
            meta={'locales': locales}, 
            *args, **kwargs)

    @classmethod
    def from_json(cls, request, *args, **kwargs):
        return cls(request, 
                   params=MultiDict(request.json_body), 
                   *args, **kwargs)

    def handle(self):
        if self.request.method in ('POST', 'PUT'):
            if self.validate():
                return True
            if not self.request.is_xhr:
                self.request.session.flash(
                    _('Your form contains errors'), 'warning')
            self.request.response.status_int = 400
        return False

    def __json__(self, request):
        return {'errors': self.errors, 'data': self.data}

    @property
    def is_multipart(self):
        for field in self:
            if field.type == 'FileField':
                return True
        return False

    @property
    def hidden_fields(self):
        return [field for field in self
                if getattr(field.widget, 'input_type', None) == 'hidden']

    @property
    def submit_fields(self):
        return [field for field in self if field.type == 'SubmitField']

    @property
    def editable_fields(self):
        non_editable_fields = self.hidden_fields + self.submit_fields
        return [field for field in self if field not in non_editable_fields]


class CSRF(BaseCSRF):

    def setup_form(self, form):
        self.request = form.request
        return super(CSRF, self).setup_form(form)

    def generate_csrf_token(self, csrf_context):
        return self.request.session.get_csrf_token()


class SecureMeta(object):
    csrf = True
    csrf_class = CSRF


class SecureForm(Form):
    class Meta(SecureMeta):
        pass
