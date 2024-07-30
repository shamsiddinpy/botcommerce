from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer, Serializer

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
            # data['is_active'] = False
            return data
        raise ValidationError("Parol to'gir kelmaydi")

    def validate_email(self, value):
        if User.objects.filter(email=value).first():
            raise ValidationError("Bu email bazada bor")
        return value


class LoginModelSerializer(Serializer):
    email = CharField(write_only=True, required=True)
    password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password')


class ForgotPasswordModelSerializer(Serializer):
    email = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email']


class ResetPasswordSerializer(Serializer):
    new_password = CharField(write_only=True, required=True)
    confirm_password = CharField(write_only=True, required=True)


