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
            'rookie_raise', 'rookie_thpc_min', 'rookie_bb_min', 'rookie_service_min',
            'rising_star_raise', 'rising_star_thpc_min', 'rising_star_bb_min', 'rising_star_service_min',
            'star_raise', 'star_thpc_min', 'star_bb_min', 'star_service_min',
            'all_star_raise', 'all_star_thpc_min', 'all_star_bb_min', 'all_star_service_min',
            'mvp_raise', 'mvp_thpc_min', 'mvp_bb_min', 'mvp_service_min',
            'mvp_platinum_raise', 'mvp_platinum_thpc_min', 'mvp_platinum_bb_min', 'mvp_platinum_service_min',
            'take_hm_bonus_lvl_1_sales_min', 'take_hm_bonus_lvl_1_multiplier',
            'take_hm_bonus_lvl_2_sales_min', 'take_hm_bonus_lvl_2_multiplier',
        ]
