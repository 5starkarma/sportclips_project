from django import forms

from apps.clients.models import Client


class ClientForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'David'}), help_text='Team leader\'s first name.')
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Alford'}), help_text='Team leader\'s last name.')
    phone = forms.CharField(min_length=10)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'support@sportclipspayroll.com'}))

    class Meta:
        model = Client
        exclude = ()
        widgets = {
            'schema_name': forms.HiddenInput(),
        }
