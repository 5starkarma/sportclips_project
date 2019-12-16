from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from phone_verify.forms import PhoneVerifyForm
from phone_verify.models import PhoneVerify


class PhoneVerifyView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = PhoneVerifyForm
    template_name = 'phone_verify/phoneverification.html'
    success_url = reverse_lazy('overview')
    success_message = 'You have successfully verified your phone number!'

    def form_valid(self, form):
        employee = self.request.user
        user_input = form.cleaned_data['passcode']
        phone_verify = get_object_or_404(PhoneVerify, employee=employee)
        if user_input == phone_verify.passcode:
            phone_verify.verified = True
            phone_verify.save()
            return super(PhoneVerifyView, self).form_valid(form)
        else:
            messages.warning(self.request, 'The passcode you entered was invalid.')
            return HttpResponseRedirect(reverse_lazy('phone-verify'))


@login_required
def resend_phone_verify(request):
    employee = request.user
    phone = employee.phone
    phone_verify, _ = PhoneVerify.objects.get_or_create(employee=employee)
    phone_verify.create_new_passcode()
    phone_verify.save()
    phone_verify.send_passcode(phone)
    return redirect('phone-verify')


@login_required
def phone_verify_check(request):
    employee = request.user
    phone_verify, _ = PhoneVerify.objects.get_or_create(employee=employee)
    if phone_verify.verified:
        return redirect('overview')
    else:
        return redirect('resend')
