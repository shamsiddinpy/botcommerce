from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from telegram.models import TelegramBot
from users.models import User


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = ['token']

