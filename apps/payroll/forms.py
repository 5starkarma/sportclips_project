from django import forms

from .models import Reports, PayrollSettings
from .payroll import get_employee_names


class UploadForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = (
            'user',
            'stylist_analysis',
            'tips_by_employee',
            'hours_week_1',
            'hours_week_2',
            'client_retention',
            'employee_service_efficiency',
        )
        exclude = ('user',)


class ManagerForm(forms.Form):
    manager = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)
        self.fields['manager'].choices = get_employee_names()


class SettingsForm(forms.ModelForm):
    class Meta:
        model = PayrollSettings
        fields = [
            'manager_service_breakpoint', 'manager_service_bonus_cap',
            'manager_service_bonus_paid_bb_min', 'manager_service_bonus_thpc_min',
            'service_bonus_sales_min', 'service_bonus_cap',
            'service_bonus_take_home_sales_min', 'service_bonus_paid_bb_min',
            'star_multiplier', 'star_thpc_min',
            'star_paid_bb_min', 'star_clients_per_hour_min',
            'all_star_multiplier', 'all_star_thpc_min',
            'all_star_paid_bb_min', 'all_star_clients_per_hour_min',
            'mvp_multiplier', 'mvp_thpc_min',
            'mvp_paid_bb_min', 'mvp_clients_per_hour_min',
            'platinum_multiplier', 'platinum_thpc_min',
            'platinum_paid_bb_min', 'platinum_clients_per_hour_min',
            'take_hm_bonus_lvl_1_sales_min', 'take_hm_bonus_lvl_1_multiplier',
            'take_hm_bonus_lvl_2_sales_min', 'take_hm_bonus_lvl_2_multiplier',
        ]
