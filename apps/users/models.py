from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.clients.models import Client


class User(AbstractUser):
    pass


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('LEADER', 'Team leader'),
        ('MANAGER', 'Manager'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    email_notifications = models.BooleanField(default=True)
    phone = models.CharField(max_length=10)
    sms_notifications = models.BooleanField(default=True)
    team_leader = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subordinates')
    tenant = models.ForeignKey(Client, on_delete=models.CASCADE)
