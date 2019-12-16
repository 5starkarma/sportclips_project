from django import forms


class PhoneVerifyForm(forms.Form):
    passcode = forms.IntegerField(min_value=1000, max_value=9999)
