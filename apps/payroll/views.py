from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from .forms import UploadForm, ManagerForm, SettingsForm
from .models import PayrollSettings, Reports, Payroll
from apps.users.models import User
from .payroll import run_payroll

import pandas as pd

pd.options.mode.chained_assignment = None


class PayrollListView(LoginRequiredMixin, ListView):
    """ Display a list of user payroll reports. """

    model = Payroll
    template_name = 'payroll/payroll_reports.html'
    context_object_name = 'payroll_reports'
    ordering = '-date_time'

    def get_queryset(self):
        queryset = super(PayrollListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


@login_required
def process_payroll(request):
    current_user = request.user._wrapped if hasattr(
        request.user, '_wrapped') else request.user
    m_form = ManagerForm(request.POST)
    if request.method == 'POST':
        m_form = ManagerForm(request.POST)
        if m_form.is_valid():

            manager_name = m_form.cleaned_data['manager']

            file_path = run_payroll(current_user, manager_name)

            static_removed_path = file_path.strip(settings.MEDIA_ROOT)

            Payroll(user=current_user, file=static_removed_path).save()

            store_owner = User.objects.filter(groups__name='owner').last()
            owner_email = store_owner.email
            send_mail(
                f'{current_user}: Payroll complete!',
                f'{current_user} has completed payroll for your Sportclips store.',
                'davidalford678@gmail.com',
                [owner_email],
                fail_silently=False,
            )
            Reports.objects.filter(user=request.user).delete()
            response = HttpResponse(open(file_path, 'rb').read())
            response['Content-Type'] = 'mimetype/submimetype'
            response['Content-Disposition'] = 'attachment; filename=payroll.xlsx'
            return response
    return render(
        request, 'payroll/select-manager-run-payroll.html', {'m_form': m_form})

#
@login_required
def payroll_preprocesses(request):
    return render(request, 'payroll/payroll.html')


class FileUploadView(LoginRequiredMixin, SuccessMessageMixin, View):
    form_class = UploadForm
    success_message = 'You have uploaded the reports. Please select a manager.'
    success_url = reverse_lazy('select_manager_run_payroll')
    template_name = 'upload.html'

    def get(self, request, *args, **kwargs):
        upload_form = self.form_class()
        return render(
            request, self.template_name, {'upload_form': upload_form})

    def post(self, request, *args, **kwargs):
        upload_form = self.form_class(
            request.POST, request.FILES)
        if upload_form.is_valid():
            form = upload_form.save(commit=False)
            form.user = self.request.user
            form.save()
            return redirect(self.success_url)
        else:
            return render(
                request, self.template_name, {'upload_form': upload_form})


@login_required()
def settings_view(request):
    payrollsettings = PayrollSettings.objects.get(id=1)
    if request.method == 'POST':
        form = SettingsForm(
            request.POST, instance=payrollsettings)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your settings have been updated!')
            return redirect('payroll')
    else:
        form = SettingsForm(instance=payrollsettings)
    context = {
        'form': form,
    }
    return render(request, 'payroll/payroll_settings.html', context)


@login_required()
def download_payroll(request):
    pass
    response = HttpResponse(open(file_path, 'rb').read())
    response['Content-Type'] = 'mimetype/submimetype'
    response['Content-Disposition'] = 'attachment; filename=payroll.xlsx'
    return response
