# api/serializer.py

from apps.users.models import *
from apps.organization.models import *
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ValidationError
from django_rest_passwordreset.serializers import PasswordTokenSerializer
from django.utils.translation import gettext_lazy as _
import jwt
import random
from .email import *
import random
from apps.users.email import send_mail, send_passwod
from django.core.cache import cache
from django.contrib.auth import authenticate, get_user_model


class LoginSerializerOTP(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class Loginserializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    token = serializers.CharField(required=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    token = serializers.CharField()
    otp = serializers.CharField(max_length=4)

    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        try:
            token = super().get_token(user)

            token["email"] = user.email
            token["is_superuser"] = user.is_superuser

            token["email"] = user.email
            token["organization"] = user.organization.id
            token["user_type"] = user.role.name
            return token
        except Exception as e:
            raise ValidationError("Something went wrong")

    def validate(self, attrs):
        decoded_token = jwt.decode(attrs["token"], j_key, algorithms=["HS256"])
        user_id = decoded_token["id"]
        cached_otp = cache.get(attrs["token"])
        if str(cached_otp) != str(attrs["otp"]):
            raise serializers.ValidationError("Invalid otp")
        user = SeteraUser.objects.get(id=user_id)

        refresh = self.get_token(user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = SeteraUser
        fields = (
            "first_name",
            "email",
            "role",
            "organization",
            "password",
            "password2",
        )

    def validate_role(self, value):
        if not value:
            raise serializers.ValidationError(
                {
                    "role": "Please Select the User Role or add Some Role(supervisor,reseller,resellerAgent,customerAdmin)"
                }
            )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        cust = Organization.objects.create(
            name=validated_data["first_name"],
        )
        user = SeteraUser.objects.create(
            first_name=validated_data["first_name"],
            email=validated_data["email"],
            role=validated_data["role"],
            organization_id=cust.id,
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserroleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = ("id", "name")
        lookup_field = "name"


class ChangePasswordSerializer(PasswordTokenSerializer):
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs


class UsersSerializers(serializers.ModelSerializer):
    role = UserroleSerializer()

    class Meta:
        model = SeteraUser
        fields = ("id", "first_name", "email", "role")


class AddUserSerilizer(serializers.Serializer):
    pass


class AdminAddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeteraUser
        fields = (
            "id",
            "first_name",
            "email",
            "role",
        )

    def create(self, validated_data):
        gen_pass = "".join((random.choice("abcdxyzpqr1234567890") for i in range(8)))
        print(gen_pass)
        validated_data["password"] = gen_pass
        user = SeteraUser.objects.create_user(**validated_data)
        send_passwod(user.email, gen_pass)
        return user








class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        # print(email)
        obj = SeteraUser.objects.filter(email=email).exists()
        if not obj:
            raise ValidationError("Email Not Exists")
        return super().validate(attrs)


class VerifyPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        label=_("confirm_password"), style={"input_type": "password"}
    )
    token = serializers.CharField()

    def validate_password(self, value):
        data = self.get_initial()
        password = data.get("confirm_password")
        confirm_password = value
        if password != confirm_password:
            raise ValidationError("Passwords and Confirm password not  matching")
        return value

    def validate_token(self, value):
        if not EmailToken.objects.filter(email_token=value).exists():
            raise serializers.ValidationError("Invalid Token")
        return value
