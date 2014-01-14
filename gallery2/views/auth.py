from pyramid.view import view_config
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPSeeOther
from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget

from ..i18n import _
from .. import models, forms, mailers


@view_config(route_name='login',
             permission=NO_PERMISSION_REQUIRED,
             renderer='login.jinja2')
def login(request):
    form = forms.LoginForm(request, redirect=request.params.get('redirect'))
    if form.handle():
        user = models.User.query.authenticate(
            form.identifier.data,
            form.password.data,
        )
        if user:
            request.messages.success(
                _('Welcome back, ${name}', mapping={'name': user.username}))
            headers = remember(request, user.id)
            redirect = form.redirect.data
            if not redirect or not redirect.startswith(request.host_url):
                redirect = request.route_url('home')
            return HTTPSeeOther(redirect, headers=headers)
        request.messages.warning(_('Sorry, invalid login'))
    return {'form': form}


@view_config(route_name='logout')
def logout(request):
    return request.seeother('home', headers=forget(request))


@view_config(route_name='signup',
             permission=NO_PERMISSION_REQUIRED,
             renderer='signup.jinja2')
def signup(request):
    form = forms.SignupForm(request)
    if form.handle():
        user = models.User()
        form.populate_obj(user)
        request.db.add(user)
        request.db.flush()
        request.messages.success(
            _('Welcome, ${name}', mapping={'name': user.username}))
        headers = remember(request, user.id)
        return request.seeother('home', headers=headers)
    return {'form': form}


@view_config(route_name='forgotpass',
             permission=NO_PERMISSION_REQUIRED,
             renderer='forgot_password.jinja2')
def forgot_password(request):

    form = forms.ForgotPasswordForm(request)
    if form.handle():
        user = models.User.query.identify(form.identifier.data)
        if user:
            user.reset_verification_code()
            request.messages.success(
                _('Check your email for your verification code'))
            request.mailer.send(mailers.forgot_password(request, user))
            return request.seeother('home')
        form.email.errors.append('No user found for this address')
    return {'form': form}


@view_config(route_name='changepass',
             permission=NO_PERMISSION_REQUIRED,
             renderer='change_password.jinja2')
def change_password(request):

    user = request.user
    verification_code = None

    if user is None:
        verification_code = request.params.get('code')
        if verification_code:
            user = models.User.query.filter_by(
                verification_code=verification_code).first()

    if user is None:
        raise NotFound()

    form = forms.ChangePasswordForm(request, code=verification_code)
    if form.handle():
        user.password = form.password.data
        user.verification_code = None
        request.messages.success(
            _('Please login again to verify your new password'))
        headers = forget(request)
        return request.seeother('login', headers=headers)
    return {'form': form}
