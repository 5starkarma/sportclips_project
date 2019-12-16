from django.urls import path

from apps.verification.views import (
    PhoneVerificationView,
    resend_phone_verification,
    check_phone_verified
)

urlpatterns = [
    path('phone-verification/', PhoneVerificationView.as_view(), name='phone-verification'),
    path('resend-phone-verification/', resend_phone_verification, name='resend-phone-verification'),
    path('check-phone-verified/', check_phone_verified, name='check-phone-verified'),
]
