from pyramid.view import view_config

from ..i18n import _
from .. import forms, models


@view_config(route_name='home',
             renderer='thumbs.jinja2')
def home(request):
    return {'images': models.Image.query}


@view_config(route_name='profile',
             renderer='thumbs.jinja2')
def profile(user, request):
    images = models.Image.query.filter_by(user=user)
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
    q = request.params.get('q', '').strip()
    if not q:
        return {'images': []}
    q = '%' + q + '%'
    images = models.Image.query.filter(
        models.Image.title.ilike(q)
    )
    return {'images': images}
