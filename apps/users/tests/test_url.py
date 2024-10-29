import pytest
from django.urls import reverse_lazy


@pytest.mark.django_db
class TestUserUrl:
    def test_user_url(self):
        sign_up_url = reverse_lazy('users:register')
        assert sign_up_url == '/api/v1/user/sign-up'

        login_url = reverse_lazy('users:login')
        assert login_url == '/api/v1/user/login'

        logout_url = reverse_lazy('users:logout')
        assert logout_url == '/api/v1/user/logout'

        confirm_url = reverse_lazy('users:activate-user', kwargs={'token': 'token'})
        assert confirm_url == '/api/v1/user/email-confirmation-message/token'

        forgot_password_url = reverse_lazy('users:forgot-password')
        assert forgot_password_url == '/api/v1/user/forgot-password'

        reset_password_message_url = reverse_lazy('users:reset-password-token', kwargs={'token': 'token'})
        assert reset_password_message_url == '/api/v1/user/reset-password-message/token'
