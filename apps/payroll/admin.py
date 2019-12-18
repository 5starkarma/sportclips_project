from django.contrib import admin

from .models import Reports, PayrollSettings, Payroll

admin.site.register(PayrollSettings)
admin.site.register(Payroll)
admin.site.register(Reports)
