from pyramid.security import NO_PERMISSION_REQUIRED, remember, forget
from pyramid.exceptions import NotFound
from pyramid.view import view_config, forbidden_view_config

from .config.i18n import _
from . import forms, models, mailers


@view_config(route_name='home',
             renderer='thumbs.jinja2')
def home(request):
    images = models.Image.query.order_by(models.Image.created_at.desc())
    return {'images': images}


@view_config(route_name='upload',
             permission='upload',
             renderer='upload.jinja2')
def upload(request):
    form = forms.UploadForm(request)
    if form.handle():
        image = models.Image(user=request.user,
                             title=form.title.data)
        image.store_image(
            form.image.data.filename,
            form.image.data.file,
            request.storage,
        )
        request.db.add(image)
        request.session.flash(
            request.localizer.translate(
                _('Your image has been uploaded')), 'success')
        return request.seeother('home')
    return {'form': form}


@view_config(route_name='search',
             renderer='thumbs.jinja2')
def search(request):
    q = request.params.get('q', None)
    if q is None:
        return {'images': []}
    images = models.Image.query.filter(
        models.Image.title.ilike('%' + q + '%')).order_by(
        models.Image.created_at.desc())
    return {'images': images}


@view_config(route_name='detail',
             renderer='detail.jinja2')
def detail(image, request):
    return {'image': image}


@forbidden_view_config(renderer='login.jinja2')
def forbidden(request):
    form = forms.LoginForm(request, action=request.route_url('login'))
    request.session.flash(
        request.localizer.translate(
            _("Sorry, you're not allowed to do that")), 'warning')
    return {'form': form}


@view_config(route_name='login',
             permission=NO_PERMISSION_REQUIRED,
             renderer='login.jinja2')
def login(request):
    form = forms.LoginForm(request)
    if form.handle():
        user = models.User.query.authenticate(
            form.identifier.data,
            form.password.data,
        )
        if user:
            request.session.flash(
                request.localizer.translate(
                    _('Welcome back, ${name}', mapping={
                        'name': user.username,
                    })),  'success')
            headers = remember(request, user.id)
            return request.seeother('home', headers=headers)
        request.session.flash('Sorry, invalid login', 'warning')
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
        request.session.flash(
            request.localizer.translate(
                _('Welcome, ${name}', mapping={
                    'name': user.username,
                })),  'success')
        headers = remember(request, user.id)
        return request.seeother('home', headers=headers)
    return {'form': form}


@view_config(route_name='forgotpass',
             permission=NO_PERMISSION_REQUIRED,
             renderer='forgot_password.jinja2')
def forgot_password(request):

    form = forms.ForgotPasswordForm(request)
    if form.handle():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            user.renew_verification_code()
            request.session.flash(
                request.localizer.translate(
                    _('Check your email for your verification code')),
                'success')
            mailers.forgot_password(request, user)
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
        request.session.flash(
            request.localizer.translate(
                _('Please login again to verify your new password')),
            'success')
        headers = forget(request)
        return request.seeother('login', headers=headers)
    return {'form': form}
