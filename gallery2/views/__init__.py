from pyramid.view import view_config
from sqlalchemy import func, not_

from ..i18n import _
from ..caching import region
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


@view_config(route_name='tags',
             renderer='tags.jinja2')
def tags(request):

    num_images = func.count(models.Image.id).label('num_images')

    tags = request.db.query(
        models.Tag.name,
        num_images,
    ).outerjoin(
        models.Image.tags
    ).filter(
        not_(models.Tag.name == None)
    ).group_by(models.Tag.name).order_by(
        models.Tag.name
    ).having(num_images > 0)

    return {'tags': tags}


@view_config(route_name='tags',
             xhr=True,
             renderer='json')
def tags_json(request):

    def _get_tags():
        return [result[0] for result in request.db.query(
            models.Tag.name
        ).order_by(models.Tag.name).all()]

    tags = region.get_or_create('tags_json', _get_tags)

    return {'tags': tags}


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
        image.taglist = form.taglist.data

        request.db.add(image)
        request.db.flush()

        request.session.flash(
            request.localizer.translate(
                _('Your image has been uploaded')), 'success')
        return request.seeother('detail', image)
    return {'form': form}


@view_config(route_name='search',
             renderer='thumbs.jinja2')
def search(request):
    q = request.params.get('q', '').strip()
    if not q:
        return {'images': []}
    causes = []
    for param in set(q.split()[:6]):
        param = '%' + param + '%'
        causes.append((
            models.Image.title.ilike(param) |
            models.Image.tagstring.ilike(param)
        ))
    images = models.Image.query.filter(*causes)
    return {'images': images}
