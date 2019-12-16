from django.urls import path

from phone_verify.views import (
    PhoneVerifyView,
    resend_phone_verify,
    phone_verify_check)

urlpatterns = [
    path('', PhoneVerifyView.as_view(), name='phone-verify'),
    path('resend/', resend_phone_verify, name='resend'),
    path('verify_redirect/', phone_verify_check, name='verify-redirect'),
]
