from pyramid.view import view_config

from ..i18n import _


@view_config(route_name='delete_comment',
             permission='delete')
def delete_comment(comment, request):
    request.db.delete(comment)
    request.messages.success(_('Your comment has been deleted'))
    return request.seeother('detail', comment.image)
