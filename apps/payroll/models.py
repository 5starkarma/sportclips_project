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
    manager_service_breakpoint = models.CharField(max_length=16, default=1870)
    manager_service_bonus_cap = models.CharField(max_length=16, default=300)
    manager_service_bonus_paid_bb_min = models.CharField(max_length=16, default=0.30)
    manager_service_bonus_thpc_min = models.CharField(max_length=16, default=1.00)

    rookie_raise = models.CharField(max_length=16, default=0.0)
    rookie_thpc_min = models.CharField(max_length=16, default=1.00)
    rookie_bb_min = models.CharField(max_length=16, default=0.35)
    rookie_service_min = models.CharField(max_length=16, default=0.0)

    rising_star_raise = models.CharField(max_length=16, default=0.5)
    rising_star_thpc_min = models.CharField(max_length=16, default=1.00)
    rising_star_bb_min = models.CharField(max_length=16, default=0.40)
    rising_star_service_min = models.CharField(max_length=16, default=38.00)

    star_raise = models.CharField(max_length=16, default=1.00)
    star_thpc_min = models.CharField(max_length=16, default=1.25)
    star_bb_min = models.CharField(max_length=16, default=0.45)
    star_service_min = models.CharField(max_length=16, default=40.00)

    all_star_raise = models.CharField(max_length=16, default=2.00)
    all_star_thpc_min = models.CharField(max_length=16, default=1.50)
    all_star_bb_min = models.CharField(max_length=16, default=0.50)
    all_star_service_min = models.CharField(max_length=16, default=42.00)

    mvp_raise = models.CharField(max_length=16, default=3.00)
    mvp_thpc_min = models.CharField(max_length=16, default=1.75)
    mvp_bb_min = models.CharField(max_length=16, default=0.55)
    mvp_service_min = models.CharField(max_length=16, default=44.00)

    mvp_gold_raise = models.CharField(max_length=16, default=4.00)
    mvp_gold_thpc_min = models.CharField(max_length=16, default=2.00)
    mvp_gold_bb_min = models.CharField(max_length=16, default=0.60)
    mvp_gold_service_min = models.CharField(max_length=16, default=46.00)

    mvp_platinum_raise = models.CharField(max_length=16, default=5.00)
    mvp_platinum_thpc_min = models.CharField(max_length=16, default=2.50)
    mvp_platinum_bb_min = models.CharField(max_length=16, default=0.65)
    mvp_platinum_service_min = models.CharField(max_length=16, default=48.00)

    take_hm_bonus_lvl_1_sales_min = models.CharField(max_length=16, default=1.00)
    take_hm_bonus_lvl_1_multiplier = models.CharField(max_length=16, default=0.10)
    take_hm_bonus_lvl_2_sales_min = models.CharField(max_length=16, default=2.00)
    take_hm_bonus_lvl_2_multiplier = models.CharField(max_length=16, default=0.20)


class Payroll(models.Model):
    file = models.FileField(upload_to='payroll')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
