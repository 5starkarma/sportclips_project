from django import forms

from apps.clients.models import Client


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First name'}), help_text='Team leader\'s first name.', label='')
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}), help_text='Team leader\'s last name.', label='')
    phone = forms.CharField(
        min_length=10,
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
        label='',
        help_text='Team leader\'s phone number.')
    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Email address'}),
        label='',
        help_text='Team leader\'s email address.')
    schema_name = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
        initial='')

    class Meta:
        model = Client
        exclude = ()
        widgets = {
            'paid_until': forms.HiddenInput(),
            'on_trial': forms.HiddenInput(),
        }
