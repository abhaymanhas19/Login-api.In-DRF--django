from django.shortcuts import render, HttpResponse

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, InvalidToken, TokenError
from rest_framework import generics
from apps.organization.models import *
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.authentication import SessionAuthentication
from django_rest_passwordreset.views import ResetPasswordConfirm
from .serializer import *
from .models import *
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics

# Create your views here.
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from .email import *
from typing import List

from django_rest_passwordreset.views import ResetPasswordConfirm

from django_rest_passwordreset.views import ResetPasswordToken
from apps.utils.orgmixin import orginizationModelMixin
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
import uuid
import jwt
import datetime
from apps.utils.utils import send_login_otp
import random

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class LoginMobileOTPAPI(APIView):
    permission_classes = ()
    serializer_class = LoginSerializerOTP

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request=request, email=email, password=password)
        if user:

            auth_token = jwt.encode(
                {
                    "email": user.email,
                    "id": user.id,
                    "otp": random.randint(1000, 9999),
                    "exp": datetime.datetime.timestamp(
                        (datetime.datetime.now() + datetime.timedelta(minutes=2))
                    ),
                },
                j_key,
                "HS256",
            )
            token_data = jwt.decode(auth_token, j_key, algorithms=["HS256"])
            del token_data["otp"]  # Remove 'otp' field from token_data
            modified_auth_token = jwt.encode(token_data, j_key, "HS256")

            if settings.DEBUG:
                send_login_otp(auth_token)
                response_token = auth_token
            else:
                send_login_otp(modified_auth_token)
                response_token = modified_auth_token

            return Response(
                {"message": "OTP Send Successfully", "token": response_token}
            )
        return Response(
            {"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class MobileAcessTokenAPI(APIView):
    permission_classes = ()
    serializer_class = Loginserializer

    def post(self, request):
        serializer = MyTokenObtainPairSerializer(
            data=request.data, context={"request": request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = SeteraUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserRoleApiview(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    queryset = UserRoles.objects.all()
    serializer_class = UserroleSerializer


class ResetPasswordConfirmView(ResetPasswordConfirm):
    serializer_class = ChangePasswordSerializer
    """
    An Api ViewSet which provides a method to reset a password based on a unique token
    """

    def post(self, request, reset_password_token, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        reset_password_token = ResetPasswordToken.objects.filter(
            key=reset_password_token
        ).first()

        def __init__(self):
            print("init")

        if reset_password_token:
            return super().post(request, *args, **kwargs)
        else:
            return Response({"message": "invaild Request or Token"})


class AdduserAPI(orginizationModelMixin, viewsets.ModelViewSet):
    serializer_class = AdminAddUserSerializer
    queryset = SeteraUser.objects.all()

    def perform_create(self, serializer):
        name = self.request.user.first_name
        obj = Organization.objects.filter(name=name).first()
        serializer.save(organization_id=obj.id)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(organization=self.request.headers["organization"])
        )


class myrole(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = UserRoles.objects.all()
    serializer_class = UserroleSerializer


class UserDetailsAPi(orginizationModelMixin, viewsets.ModelViewSet):
    serializer_class = UsersSerializers
    http_method_names: List[str] = ["get", "patch"]
    queryset = SeteraUser.objects.all()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(organization=self.request.headers["organization"])
        )
