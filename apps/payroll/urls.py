from django.urls import path
from apps.payroll import views as payroll_views

urlpatterns = [
    path('reports/', payroll_views.PayrollListView.as_view(), name='reports'),
    path('upload/', payroll_views.FileUploadView.as_view(), name='upload'),
    path('select-manager/', payroll_views.process_payroll, name='select-manager'),
    path('settings/', payroll_views.settings_view, name='settings'),
    path('<int:pk>/download/', payroll_views.download_payroll, name='download'),
]
