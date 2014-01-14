from pyramid.view import view_config

from ..i18n import _
from .. import models, forms


@view_config(route_name='detail',
             renderer='detail.jinja2')
def detail(image, request):
    form = forms.CommentForm(
        request, action=request.route_url('add_comment', image))
    return {'image': image, 'comment_form': form}


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
        request.messages.success(_('Your image has been updated'))
        return request.seeother('detail', image)
    return {'image': image, 'form': form}


@view_config(route_name='delete',
             permission='delete')
def delete(image, request):
    request.db.delete(image)
    request.storage.delete(image.image)
    request.storage.delete(image.thumbnail)
    request.messages.danger(_('Your image has been deleted'))
    return request.seeother('home')


@view_config(route_name='add_comment',
             renderer='detail.jinja2',
             request_method='POST',
             permission='add_comment')
def add_comment(image, request):
    form = forms.CommentForm(request)
    if form.handle():
        models.Comment(author=request.user,
                       image=image,
                       comment=form.comment.data)

        request.messages.success(_('Thanks for your comment'))
        return request.seeother('detail', image)
    return {'comment_form': form, 'image': image}
