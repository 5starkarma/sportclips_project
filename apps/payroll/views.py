from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from .forms import UploadForm, ManagerForm, SettingsForm
from .models import PayrollSettings, Reports, Payroll
from .payroll import run_payroll

import pandas as pd

pd.options.mode.chained_assignment = None


class FileUploadView(LoginRequiredMixin, SuccessMessageMixin, View):
    form_class = UploadForm
    success_message = 'You have uploaded the reports. Please select a manager.'
    success_url = reverse_lazy('select-manager')
    template_name = 'payroll/upload.html'

    def get(self, request, *args, **kwargs):
        upload_form = self.form_class()
        return render(
            request, self.template_name, {'upload_form': upload_form})

    def post(self, request, *args, **kwargs):
        upload_form = self.form_class(request.POST, request.FILES)
        if upload_form.is_valid():
            form = upload_form.save(commit=False)
            form.user = self.request.user
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'upload_form': upload_form})


class PayrollListView(LoginRequiredMixin, ListView):
    model = Payroll
    template_name = 'payroll/reports.html'
    context_object_name = 'reports'
    ordering = '-date_time'


@login_required
def process_payroll(request):
    if request.method == 'POST':
        m_form = ManagerForm(request.POST)
        if m_form.is_valid():
            current_user = request.user
            manager_name = m_form.cleaned_data['manager']
            file_path = run_payroll(manager_name)
            static_removed_path = file_path.strip(settings.MEDIA_ROOT)
            Payroll(user=current_user, file=static_removed_path).save()
            Reports.objects.filter(user=request.user).delete()
            response = HttpResponse(open(file_path, 'rb').read())
            response['Content-Type'] = 'mimetype/submimetype'
            response['Content-Disposition'] = 'attachment; filename=payroll.xlsx'
            return response
    else:
        m_form = ManagerForm()
    return render(request, 'payroll/select-manager.html', {'m_form': m_form})


@login_required
@permission_required('payroll.change_user', raise_exception=True)
def settings_view(request):
    instance, _ = PayrollSettings.objects.get_or_create(id=1)
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'Payroll settings have been saved!')
            return redirect('upload')
    else:
        form = SettingsForm(instance=instance)
    context = {'form': form}
    return render(request, 'payroll/settings.html', context)


@login_required
def download_payroll(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    filepath = settings.MEDIA_ROOT + '/payroll' + payroll.file.url.replace('/media/', '')
    response = HttpResponse(open(filepath, 'rb').read())
    response['Content-Type'] = 'mimetype/submimetype'
    response['Content-Disposition'] = 'attachment; filename=payroll.xlsx'
    return response
