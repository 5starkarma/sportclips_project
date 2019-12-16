from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        help_text='Choose a username.',
        label='')
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First name'}),
        help_text='Your first name.',
        label='')
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
        help_text='Your last name.',
        label='')
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email address'}),
        help_text='Your email address.',
        label='')
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
        help_text='Your phone number.',
        label='')
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Password'}),
        help_text='Create a strong password',
        label='')
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Repeat password'}),
        help_text='Repeat the password',
        label='')
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
