from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.clients.models import Client


class User(AbstractUser):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=10)
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    tenant = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
