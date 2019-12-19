from django.urls import path
from django.contrib.auth import views as auth_views

from apps.users import views
from apps.users.views import UserListView, UserUpdateView

urlpatterns = [
    path('register/', views.user_register, name='users-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/', UserListView.as_view(), name='accounts'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
