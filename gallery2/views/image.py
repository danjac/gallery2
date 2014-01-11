from pyramid.view import view_config

from ..i18n import _
from .. import forms


@view_config(route_name='detail',
             renderer='detail.jinja2')
def detail(image, request):
    return {'image': image}


@view_config(route_name='edit',
             renderer='edit.jinja2',
             permission='edit')
def edit(image, request):
    # not using obj due to taglist
    form = forms.EditForm(request,
                          title=image.title,
                          taglist=image.tagstring)
    if form.handle():
        image.title = form.title.data
        image.taglist = form.taglist.data
        request.session.flash(
            request.localizer.translate(
                _('Your image has been updated')), 'success')
        return request.seeother('detail', image)
    return {'image': image, 'form': form}


@view_config(route_name='delete',
             permission='delete')
def delete(image, request):
    request.db.delete(image)
    request.storage.delete(image.image)
    request.storage.delete(image.thumbnail)
    request.session.flash(
        request.localizer.translate(
            _('Your image has been deleted')), 'danger')
    return request.seeother('home')
