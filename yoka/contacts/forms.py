from django import forms
from django.utils.translation import gettext_lazy as _

from yoka.contacts.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("email", "subject", "message")
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }
        error_messages = {
            "subject": {
                "max_length": _("%(limit_value)d文字以内で入力して下さい。 %(show_value)d 文字あります。"),
            },
            "message": {
                "max_length": _("%(limit_value)d文字以内で入力して下さい。 %(show_value)d 文字あります。"),
            },
        }