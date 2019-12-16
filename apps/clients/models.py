from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    paid_until = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True

    def __str__(self):
        return str(self.schema_name)


class Domain(DomainMixin):
    pass
