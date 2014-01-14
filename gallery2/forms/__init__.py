from wtforms import (
    StringField,
    TextAreaField,
    HiddenField,
    FileField,
    PasswordField,
    SubmitField,
    ValidationError,
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)

from wtforms_alchemy import Unique

from ..models import User
from ..i18n import _
from .base import SecureForm
from .validators import FileRequired


MIN_PASSWORD_LENGTH = 6


class CommentForm(SecureForm):

    comment = TextAreaField(_("Add your comment"), [DataRequired()])
    submit = SubmitField(_("Add comment"))


class EditForm(SecureForm):

    title = StringField(_("Title"), [DataRequired()])
    taglist = StringField(_("Tags"))
    submit = SubmitField(_("Save"))


class UploadForm(SecureForm):

    title = StringField(_("Title"))
    image = FileField(_("Image"), [FileRequired()])
    taglist = StringField(_("Tags"))
    submit = SubmitField(_("Upload"))

    def validate_image(self, field):
        filename = getattr(field.data, 'filename', None)
        if filename and not self.request.storage.filename_allowed(filename):
            raise ValidationError(_("Must be an image"))


class LoginForm(SecureForm):

    identifier = StringField(_("Email or username"), [DataRequired()])
    password = PasswordField(_("Password"), [DataRequired()])
    redirect = HiddenField()
    submit = SubmitField(_("Login"))


class SignupForm(SecureForm):
    username = StringField(_("Username"), [
        DataRequired(),
        Unique(User.username),
    ])
    email = StringField(_("Email address"), [
        Email(),
        Unique(User.email),
    ])
    password = PasswordField(
        _("Password"), [
            DataRequired(),
            Length(min=MIN_PASSWORD_LENGTH)
        ]
    )
    password_confirm = PasswordField(
        _("Password confirm"),
        [EqualTo('password')]
    )
    submit = SubmitField(_("Signup"))


class ForgotPasswordForm(SecureForm):
    identifier = StringField("Email or username", [DataRequired()])
    submit = SubmitField("Send")


class ChangePasswordForm(SecureForm):
    password = PasswordField(
        _("Password"), [
            DataRequired(),
            Length(min=MIN_PASSWORD_LENGTH)
        ]
    )
    password_confirm = PasswordField(
        _("Password confirm"),
        [EqualTo('password')]
    )
    submit = SubmitField("Signup")
