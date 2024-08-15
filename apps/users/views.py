from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     get_object_or_404)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
            return redirect('users:login')
        return Response({"error": "The link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class LoginViewAPIView(GenericAPIView):
    serializer_class = LoginModelSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


@extend_schema(tags=['Authentication'])
class LogoutAPIView(GenericAPIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Muvaffaqiyatli chiqish amalga oshirildi"})


@extend_schema(tags=['Authentication'])
class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Biz sizning elektron pochtangizga parolni tiklash havolasini yubordik..!!!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Authentication'])
class ResetPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        email = cache.get(token)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user = get_object_or_404(User, email=email)
            user.set_password(new_password)
            user.save()
            cache.delete(token)
            return redirect('users:login')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
