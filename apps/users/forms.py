from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    sms_notifications = forms.BooleanField(
        initial=True,
        required=False)
    email_notifications = forms.BooleanField(
        initial=True,
        required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password1',
            'password2',
            'sms_notifications',
            'email_notifications',
        ]
        widgets = {
            'tenant': forms.HiddenInput()
        }
