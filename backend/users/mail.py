from core import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from utils.exceptions import AlreadyVerified

from .models import EmailValidationToken, User


def send_validation_mail(email: str):
    user = User.objects.get(email=email)

    if user.email_validated:
        raise AlreadyVerified()
    else:
        token = get_random_string(64)
        EmailValidationToken.objects.filter(user=user).delete()
        EmailValidationToken.objects.create(user=user, token=token)
        subject = 'Please confirm your email address'
        url = f'{settings.REDIRECT_URL}/users/email-validation/confirm/?token='
        message = (
            'This is a validation from Zweb, please verify your email with the link'
            + f'. Or you can input {token} manually to activate your account.'
        )
        from_email = 'Zweb <noreply@zweb.com>'
        recipient_list = [email]
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            html_message=f'{message}<br><a href={url}{token}>{url}{token}</a>',
        )
        return ({'title': 'Success', 'detail': 'Validation email sent.'},)
