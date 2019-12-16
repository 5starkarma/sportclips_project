from django.urls import path

from apps.users import views

urlpatterns = [
    path('', views.user_register, name='users-register'),
]
