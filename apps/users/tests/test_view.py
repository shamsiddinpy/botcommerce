import pytest

from users.views import User


@pytest.mark.django_db
class TestUserView:
    def test_create_user(self, user_test):
        user = User.objects.create_user(**user_test)
        assert user.email == user_test['email']
        assert user.password == user_test['password']

    def test_create_superuser(self, user_test):
        superuser = User.objects.create_superuser(**user_test)
        assert superuser.is_active
        assert superuser.public_offer


@pytest.mark.django_db
class TestUserView:
    pass
