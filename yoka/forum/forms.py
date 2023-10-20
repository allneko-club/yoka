from django import forms

from .models import Reply, Thread


class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title", "category", "handle_name", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "handle_name": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class UpdateThreadForm(forms.ModelForm):
    """
    save()や__init__はModelFormクラスのを使う。
    """

    class Meta(CreateThreadForm.Meta):
        """MetaクラスはCreateThreadFormクラスのMetaクラスを使う"""
        pass


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["handle_name", "content"]
        widgets = {
            "handle_name": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        self.thread_id = kwargs.pop("thread_id")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super().save(commit=False)
        inst.user = self.user
        inst.thread_id = self.thread_id
        if commit:
            inst.save()
            self.save_m2m()
        return inst
