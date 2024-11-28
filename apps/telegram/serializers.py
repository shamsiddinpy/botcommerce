from celery.worker.state import requests
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from telegram.models import TelegramBot
from users.models import User

import requests  # To'g'ri modulni import qilamiz


def is_valid_telegram_bot(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url)  # API so'rov yuboriladi
    if response.status_code == 200:
        data = response.json()
        return data.get("ok", False)  # "ok" qiymatini tekshiramiz
    return False


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = ['token']

    def validate(self, attrs):
        token = attrs['token']
        if not is_valid_telegram_bot(attrs):
            raise serializers.ValidationError({"error": "The token is invalid. Please enter a valid token."})
        return attrs
