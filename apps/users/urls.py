from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import (ForgotPasswordView, LoginViewAPIView,
                         LogoutGenericAPIView, RegisterViewCreateAPIView,
                         ResetPasswordView, UserActivateView)

urlpatterns = [

    path('sign-up', RegisterViewCreateAPIView.as_view(), name='register'),
    path('login', LoginViewAPIView.as_view(), name='login'),
    path('logout', LogoutGenericAPIView.as_view(), name='logout'),
    path('email-confirmation-message/<str:token>', UserActivateView.as_view(), name='activate_user'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password-message/<str:token>', ResetPasswordView.as_view(), name='reset_password_token', )
]

router = DefaultRouter()
# router.register('shop', ShopModelSerializer, basename='shop')
