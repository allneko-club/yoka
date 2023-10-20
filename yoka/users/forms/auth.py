from django import forms
from django.contrib.auth import forms as admin_forms, get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AuthenticationForm(admin_forms.AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("このユーザー名は使用できません。")},
        }
        fields = ["username", "email", "password1", "password2", "accept_rule"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "accept_rule": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    def clean_accept_rule(self):
        value = self.cleaned_data["accept_rule"]
        if not value:
            raise ValidationError(_("利用規約に同意して下さい。"), code="not_accept_rule")
        return value


class PasswordChangeForm(admin_forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs["class"] = "form-control"
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"


class PasswordResetForm(admin_forms.PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"


class SetPasswordForm(admin_forms.SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs["class"] = "form-control"
        self.fields["new_password2"].widget.attrs["class"] = "form-control"
