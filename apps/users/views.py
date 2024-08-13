from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     get_object_or_404)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from shared.utils.email_message import send_email, send_password_reset_email
from users.models import User
from users.serializer import (ForgotPasswordModelSerializer,
                              LoginModelSerializer, ResetPasswordSerializer,
                              UserSerializerModelSerializer)

User = get_user_model()


@extend_schema(tags=['Authentication'])
class RegisterViewCreateAPIView(CreateAPIView):
    serializer_class = UserSerializerModelSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            token = get_random_string(32)
            cache.set(token, user.email, 3600)
            response = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'invitation_code': user.invitation_code,
                'language': user.language,
            }
            send_email(user.email, token)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Authentication'])
class UserActivateView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        data = cache.get(token)
        if data:
            user = get_object_or_404(User, email=data)
            user.is_active = True
            user.public_offer = True
            cache.delete(token)
            user.save()
            return redirect('login')
        return Response({"error": "Havola noto'g'ri yoki muddati o'tgan."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class LoginViewAPIView(APIView):
    serializer_class = LoginModelSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Email yoki parol noto'g'ri."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class LogoutAPIView(APIView):  # lagout ishlmaypdi
    def post(self, request):
        try:
            refresh_token = request.data["token"]
            refresh_token.delete()
            return Response({"detail": "Muvaffaqiyatli chiqish amalga oshirildi."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Noto'g'ri token"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordModelSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']

        if not email:
            return Response({"message": f"Emailni kiriting..!!!"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)
        token = get_random_string(32)
        cache.set(token, user.email, 3600)
        send_password_reset_email(user.email, token)
        return Response({"Message": "Parolni tiklash havolasi emailzga yubordik..!"}, status=status.HTTP_200_OK)


@extend_schema(tags=['Authentication'])
class ResetPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        email = cache.get(token)
        if not email:
            return Response({"errors": "Yangi barol qo'ying bir xil bo'lish kerak emas"})
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            if new_password:
                user = get_object_or_404(User, email=email)
                user.set_password(new_password)
                cache.delete(token)
                user.save()
                return redirect('login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
