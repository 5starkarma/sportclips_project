from django.urls import path, reverse_lazy
from . import views as payroll_views

urlpatterns = [
    path('payroll/', payroll_views.payroll_preprocesses, name='payroll'),
    path('payroll_reports/', payroll_views.PayrollListView.as_view(
        template_name='payroll/payroll_reports.html'),
         name='payroll_reports'),
    path('upload/', payroll_views.FileUploadView.as_view(
        success_url=reverse_lazy('select_manager_run_payroll'),
        template_name='payroll/upload.html'),
        name='upload'),
    path('select-manager-run-payroll/',
         payroll_views.process_payroll,
         name='select_manager_run_payroll'),
    path('settings/', payroll_views.settings_view, name='settings'),
]
