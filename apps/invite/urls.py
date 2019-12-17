from django.urls import path

from apps.invite.views import InviteView

urlpatterns = [
    path('invite/', InviteView.as_view(), name='invite'),
]
