from pyramid.view import forbidden_view_config, notfound_view_config

from ..i18n import _
from .. import forms


@notfound_view_config(renderer='404.jinja2')
def not_found(request):
    request.response.status_int = 404
    return {}


@forbidden_view_config(renderer='login.jinja2')
def forbidden(request):
    form = forms.LoginForm(request, action=request.route_url('login'))
    request.session.flash(
        request.localizer.translate(
            _("Sorry, you're not allowed to do that")), 'warning')
    request.response.status_int = 403
    return {'form': form}
