from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["address", "sex"]
        widgets = {
            "address": forms.Select(attrs={"class": "form-select"}),
            "sex": forms.Select(attrs={"class": "form-select"}),
        }
        error_messages = {
            "address": {
                "invalid_choice": _("選択肢の中から選んでください"),
            },
            "sex": {
                "invalid_choice": _("選択肢の中から選んでください"),
            },
        }


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
