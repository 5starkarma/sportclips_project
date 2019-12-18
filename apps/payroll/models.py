from django.db import models
from apps.users.models import User


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.username, filename)


class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    stylist_analysis = models.FileField(upload_to=user_directory_path)
    tips_by_employee = models.FileField(upload_to=user_directory_path)
    hours_week_1 = models.FileField(upload_to=user_directory_path)
    hours_week_2 = models.FileField(upload_to=user_directory_path)
    client_retention = models.FileField(upload_to=user_directory_path)
    employee_service_efficiency = models.FileField(upload_to=user_directory_path)


class PayrollSettings(models.Model):
    manager_service_breakpoint = models.CharField(max_length=16)
    manager_service_bonus_cap = models.CharField(max_length=16)
    manager_service_bonus_paid_bb_min = models.CharField(max_length=16)
    manager_service_bonus_thpc_min = models.CharField(max_length=16)
    service_bonus_sales_min = models.CharField(max_length=16)
    service_bonus_cap = models.CharField(max_length=16)
    service_bonus_take_home_sales_min = models.CharField(max_length=16)
    service_bonus_paid_bb_min = models.CharField(max_length=16)
    star_multiplier = models.CharField(max_length=16)
    star_thpc_min = models.CharField(max_length=16)
    star_paid_bb_min = models.CharField(max_length=16)
    star_clients_per_hour_min = models.CharField(max_length=16)
    all_star_multiplier = models.CharField(max_length=16)
    all_star_thpc_min = models.CharField(max_length=16)
    all_star_paid_bb_min = models.CharField(max_length=16)
    all_star_clients_per_hour_min = models.CharField(max_length=16)
    mvp_multiplier = models.CharField(max_length=16)
    mvp_thpc_min = models.CharField(max_length=16)
    mvp_paid_bb_min = models.CharField(max_length=16)
    mvp_clients_per_hour_min = models.CharField(max_length=16)
    platinum_multiplier = models.CharField(max_length=16)
    platinum_thpc_min = models.CharField(max_length=16)
    platinum_paid_bb_min = models.CharField(max_length=16)
    platinum_clients_per_hour_min = models.CharField(max_length=16)
    take_hm_bonus_lvl_1_sales_min = models.CharField(max_length=16)
    take_hm_bonus_lvl_1_multiplier = models.CharField(max_length=16)
    take_hm_bonus_lvl_2_sales_min = models.CharField(max_length=16)
    take_hm_bonus_lvl_2_multiplier = models.CharField(max_length=16)


class Payroll(models.Model):
    file = models.FileField(upload_to='payroll')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
