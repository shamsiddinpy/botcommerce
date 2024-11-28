from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from telegram.serializers import TelegramUserSerializer


# Create your views here.
@extend_schema(tags=['Telegram'])
class TokenCreateAPIView(CreateAPIView):
    serializer_class = TelegramUserSerializer
