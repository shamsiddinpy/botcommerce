from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer, Serializer

from shared.utils.email_message import send_email, send_password_reset_email
from users.models import User


class UserSerializerModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, required=True)
    email = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'confirm_password', 'type', 'invitation_code')
        extra_kwargs = {
            'password':
                {
                    'write_only': True
                }
        }

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password == data['password']:
            data['password'] = make_password(data['password'])
            return data
        raise ValidationError("Parol to'gir kelmaydi")

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError("Bu email bazada bor")
        return value

    def save(self, request=None, **kwargs):
        user = super().save(**kwargs)
        token = get_random_string(32)
        cache.set(token, user.email, 3600)
        request = self.context.get('request')
        if request:
            send_email(request, user.email, token)
        return user


class LoginModelSerializer(Serializer):
    email = CharField(write_only=True, required=True)
    password = CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.pop('email')
        password = data.pop('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise ValidationError("Email yoki parol noto'g'ri.")
            data['user'] = user
        else:
            raise ValidationError("Email yoki parol noto'g'ri.")
        return data

    class Meta:
        fields = ('email', 'password')


class ForgotPasswordModelSerializer(Serializer):
    email = CharField(write_only=True, required=True)

    def validate_email(self, value):
        if not value:
            raise ValidationError({"message", "Enter email..!!!"})
        if not User.objects.filter(email=value).exists():
            raise ValidationError({"error": "Bu e-pochtaga ega foydalanuvchi mavjud emas."})
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = get_random_string(32)
        cache.set(token, user.email, 3600)
        request = self.context.get('request')
        if request:
            send_password_reset_email(request, user.email, token)
        return user


class ResetPasswordSerializer(Serializer):
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("r")
        return data
