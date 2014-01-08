from pyramid.view import forbidden_view_config

from ..i18n import _
from .. import forms


@forbidden_view_config(renderer='login.jinja2')
def forbidden(request):
    form = forms.LoginForm(request, action=request.route_url('login'))
    request.session.flash(
        request.localizer.translate(
            _("Sorry, you're not allowed to do that")), 'warning')
    return {'form': form}
