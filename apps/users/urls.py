from django.urls import path
from users.views import (ForgotPasswordView, LoginViewAPIView, LogoutAPIView,
                         RegisterViewCreateAPIView, ResetPasswordView,
                         UserActivateView)

# app_nom = 'users'
urlpatterns = [

    path('sign-up', RegisterViewCreateAPIView.as_view(), name='register'),
    path('login', LoginViewAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('email-confirmation-message/<str:token>', UserActivateView.as_view(), name='activate_user'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password-message/<str:token>', ResetPasswordView.as_view(), name='reset_password_token', )
]
