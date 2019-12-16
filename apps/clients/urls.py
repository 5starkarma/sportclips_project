from django.urls import path

from apps.clients import views

urlpatterns = [
    path('', views.tenant_register, name='landing'),
]
