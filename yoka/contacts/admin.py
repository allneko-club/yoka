from django.contrib import admin

from yoka.contacts.models import Contact, ContactStatus


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact


@admin.register(ContactStatus)
class ContactStatusAdmin(admin.ModelAdmin):
    model = ContactStatus
