from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView, LoginView, PasswordResetView, PasswordResetDoneView,
    PasswordResetCompleteView, PasswordResetConfirmView,
)
from .views import new_account

app_name = 'accounts'

urlpatterns = [
    path('new_account/', new_account, name='new_account'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name = 'accounts/login.html'), name='login'),
    path('reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')), name='reset'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete')
]
