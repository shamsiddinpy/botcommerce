from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from users.models import User


def send_email(email: str, confirmation_code: str):
    link = f'http://localhost:8000/api/v1/users/email-confirmation-message/{confirmation_code}'

    context = {
        'link': link
    }

    html_message = render_to_string('users/email.html', context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject='Salom, xush kelibsiz BotCommerce',
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()


def send_password_reset_email(email: str, confirmation_code: str):
    link = f'http://localhost:8000/api/v1/users/reset-password-message/{confirmation_code}'

    context = {
        'link': link
    }

    html_message = render_to_string('users/resid_email.html', context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject="Parolni tiklash - BotCommerce",
        body=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()

