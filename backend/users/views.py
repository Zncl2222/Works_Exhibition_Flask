from django.shortcuts import redirect
from django.utils import timezone
from core import settings

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer

from .models import EmailValidationToken
from .serializers import EmailTokenValidationSerializer
from .mail import send_validation_mail


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        send_validation_mail(serializer.validated_data['email'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
