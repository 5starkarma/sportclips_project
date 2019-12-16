from django.db import models

from apps.users.models import User
from configs.settings import account_sid, auth_token, sportclips_phone

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from random import randint


class PhoneVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passcode = models.PositiveIntegerField(null=True)
    datetime = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def create_new_passcode(self):
        self.passcode = randint(10000, 99999)
        self.save()

    def send_passcode(self, phone):
        try:
            client = Client(account_sid, auth_token)
            client.messages.create(
                body=f"Your SC payroll phone verification code is: {self.passcode}",
                from_=sportclips_phone,
                to='1' + str(phone))
        except TwilioRestException:
            pass
