from django.urls import path, include
from apps.users import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django_rest_passwordreset.urls import reset_password_request_token
from django_rest_passwordreset import urls

router = DefaultRouter()
router.register("add-role", views.UserRoleApiview, basename="addrole")
router.register("users", views.UserDetailsAPi, basename="user")
router.register("add-user", views.AdduserAPI, basename="adduser")

urlpatterns = [
    path("login/", views.LoginMobileOTPAPI.as_view(), name="login"),
    path("otp-verify/", views.MobileAcessTokenAPI.as_view(), name="otp-verify"),
    path("forget-password/", views.ForgetApiView.as_view(), name="forget_password"),
    path("confirm/<token>/", views.VerifyResetPassword.as_view(), name="confirm_passowrd"  ),
    # path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", views.RegisterView.as_view(), name="auth_register"),
    path(
        "password_reset/", reset_password_request_token, name="reset-password-request"
    ),
    path(
        "confirm/<reset_password_token>/",
        views.ResetPasswordConfirmView.as_view(),
        name="confirm_passowrd",
    ),
] + router.urls
