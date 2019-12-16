from django import forms


class PhoneVerificationForm(forms.Form):
    passcode = forms.IntegerField(min_value=10000, max_value=99999)
