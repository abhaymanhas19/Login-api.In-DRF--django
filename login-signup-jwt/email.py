from apps.organization.models import *

from .serializer import *
from .models import *

# Create your views here.
from my_backend.settings.base import *
from my_backend.settings.production import *
from my_backend.settings.development import *
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    # email_plaintext_message = "http://127.0.0.1:8000{}?token={}".format(reverse('confirm/<token>/:confirm_passowrd'), reset_password_token.key)
    #     # title:

    email_plaintext_message = (
        f"http://127.0.0.1:8000/confirm/{reset_password_token.key}"
    )

    subject = "Password Reset for {title}".format(title="Some website title")
    # message:
    message = email_plaintext_message
    # from:
    email_from = EMAIL_HOST

    # to:
    send_mail(subject, message, email_from, [reset_password_token.user.email])
    print("send")


# Create your views here.


def send_passwod(email, password):
    subject = "Your account login Password"
    message = f"your Otp is {password}"
    email_from = EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    print("Done")
