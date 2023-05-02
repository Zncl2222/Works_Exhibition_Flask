from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils import timezone
from ZWeb_app import settings
from django.utils.crypto import get_random_string

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer

from .models import EmailValidationToken, User
from .serializers import EmailValidationSerializer, EmailTokenValidationSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmailValidationView(generics.CreateAPIView):
    serializer_class = EmailValidationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            if user.email_validated:
                return Response(
                    {'detail': 'Email already validated.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                token = get_random_string(64)
                EmailValidationToken.objects.filter(user=user).delete()
                EmailValidationToken.objects.create(user=user, token=token)
                subject = 'Please confirm your email address'
                url = f'{settings.REDIRECT_URL}/users/email-validation/confirm/'
                message = 'This is a validation from Zweb, please verify your email with the link'
                from_email = 'Zweb <noreply@zweb.com>'
                recipient_list = [email]
                send_mail(
                    subject,
                    message,
                    from_email,
                    recipient_list,
                    html_message=f'{message}<br><a href={url}{token}>{url}{token}</a>',
                )
                return Response(
                    {'detail': 'Validation email sent.'},
                    status=status.HTTP_201_CREATED,
                )
        else:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )


class EmailValidationConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailTokenValidationSerializer

    def email_validation(self, token):
        try:
            email_validation_token = EmailValidationToken.objects.get(token=token)
        except EmailValidationToken.DoesNotExist:
            return Response(
                {'detail': 'Invalid token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = email_validation_token.user
        if user.email_validated:
            return Response(
                {'detail': 'Email already validated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        time_diff = (timezone.now() - email_validation_token.created_at).total_seconds() / 60
        if time_diff > 10:
            return Response(
                {'detail': 'Token is expired, please re-send a new token and validate again.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.email_validated = True
        user.save()
        email_validation_token.delete()
        return redirect(settings.REDIRECT_URL)

    def get(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        return self.email_validation(token)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        return self.email_validation(token)
