from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, TemplateView

from yoka.contacts.forms import ContactForm
from yoka.contacts.models import Contact
from yoka.contacts.signals import contact_done


class ContactCreateView(CreateView):
    """問い合わせページ"""
    model = Contact
    form_class = ContactForm
    success_url = reverse_lazy("contacts:contact_done")
    extra_context = {"title": _("お問い合わせ")}

    def form_valid(self, form):
        ctx = self.get_context_data(form=form)
        if self.request.POST.get("next") == "confirm":
            return render(self.request, "contacts/contact_confirm.html", ctx)
        if self.request.POST.get("next") == "submit":
            self.object = form.save()
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]
            contact_done.send(
                sender=self.__class__,
                email=email,
                subject=subject,
                message=message,
            )
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ContactDoneView(TemplateView):
    """問い合わせ完了ページ"""
    template_name = "contacts/contact_done.html"
    extra_context = {"title": _("お問い合わせ完了")}
