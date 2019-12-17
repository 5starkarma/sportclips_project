from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.users.models import User
from apps.verification.forms import PhoneVerificationForm
from apps.verification.models import PhoneVerification


@login_required
def resend_phone_verification(request):
    pv_object, _ = PhoneVerification.objects.get_or_create(user=request.user)
    pv_object.create_new_passcode()
    pv_object.save()
    pv_object.send_passcode(request.user.phone)
    return redirect('phone-verification')


@login_required
def check_phone_verified(request):
    pv_object, _ = PhoneVerification.objects.get_or_create(user=request.user)
    if pv_object.verified:
        user_count = User.objects.filter(tenant=request.tenant).count()
        if user_count == 1:
            return redirect('invite')
        else:
            return redirect('main')
    else:
        return redirect('resend-phone-verification')


class PhoneVerificationView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = PhoneVerificationForm
    template_name = 'phone_verify/phone_verification.html'
    success_url = reverse_lazy('main')
    success_message = 'You have successfully verified your phone number!'

    def form_valid(self, form):
        phone_verify = get_object_or_404(PhoneVerification, user=self.request.user)
        if form.cleaned_data['passcode'] == phone_verify.passcode:
            phone_verify.verified = True
            phone_verify.save()
            return super(PhoneVerificationView, self).form_valid(form)
        else:
            messages.warning(self.request, 'The passcode you entered was invalid.')
            return HttpResponseRedirect(reverse_lazy('phone-verify'))
