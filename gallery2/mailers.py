from .lib.mail import get_rendered_mail


def forgot_password(request, user):

    return get_rendered_mail(
        request,
        subject='Recover your password',
        recipients=[user.email],
        renderer='forgot_password',
        context={
            'user': user,
        }
    )
