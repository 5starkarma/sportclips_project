from django import forms

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from configs.settings import account_sid, auth_token, sportclips_phone


class InviteForm(forms.Form):
    name = forms.CharField()
    phone = forms.CharField(max_length=10, min_length=10)
    message = forms.CharField(widget=forms.Textarea)

    def send_sms(self):
        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=self.cleaned_data['message'], from_=sportclips_phone, to=str(self.cleaned_data['phone']))
        except TwilioRestException:
            pass
