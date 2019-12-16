from django.contrib import admin

from apps.clients.models import Client, Domain

admin.site.register(Client)
admin.site.register(Domain)
