# Generated by Django 2.2.7 on 2019-12-17 21:48

import apps.payroll.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_service_breakpoint', models.CharField(max_length=16)),
                ('manager_service_bonus_cap', models.CharField(max_length=16)),
                ('manager_service_bonus_paid_bb_min', models.CharField(max_length=16)),
                ('manager_service_bonus_thpc_min', models.CharField(max_length=16)),
                ('service_bonus_sales_min', models.CharField(max_length=16)),
                ('service_bonus_cap', models.CharField(max_length=16)),
                ('service_bonus_take_home_sales_min', models.CharField(max_length=16)),
                ('service_bonus_paid_bb_min', models.CharField(max_length=16)),
                ('star_multiplier', models.CharField(max_length=16)),
                ('star_thpc_min', models.CharField(max_length=16)),
                ('star_paid_bb_min', models.CharField(max_length=16)),
                ('star_clients_per_hour_min', models.CharField(max_length=16)),
                ('all_star_multiplier', models.CharField(max_length=16)),
                ('all_star_thpc_min', models.CharField(max_length=16)),
                ('all_star_paid_bb_min', models.CharField(max_length=16)),
                ('all_star_clients_per_hour_min', models.CharField(max_length=16)),
                ('mvp_multiplier', models.CharField(max_length=16)),
                ('mvp_thpc_min', models.CharField(max_length=16)),
                ('mvp_paid_bb_min', models.CharField(max_length=16)),
                ('mvp_clients_per_hour_min', models.CharField(max_length=16)),
                ('platinum_multiplier', models.CharField(max_length=16)),
                ('platinum_thpc_min', models.CharField(max_length=16)),
                ('platinum_paid_bb_min', models.CharField(max_length=16)),
                ('platinum_clients_per_hour_min', models.CharField(max_length=16)),
                ('take_hm_bonus_lvl_1_sales_min', models.CharField(max_length=16)),
                ('take_hm_bonus_lvl_1_multiplier', models.CharField(max_length=16)),
                ('take_hm_bonus_lvl_2_sales_min', models.CharField(max_length=16)),
                ('take_hm_bonus_lvl_2_multiplier', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stylist_analysis', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('tips_by_employee', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('hours_week_1', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('hours_week_2', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('client_retention', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('employee_service_efficiency', models.FileField(upload_to=apps.payroll.models.user_directory_path)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='payroll')),
                ('date_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]