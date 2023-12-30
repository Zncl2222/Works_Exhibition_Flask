import os

from core import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .mail import send_validation_mail
from .models import EmailValidationToken
from .serializers import EmailTokenValidationSerializer, UserSerializer

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class OAuthViewset(GenericViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_path='google-login')
    def google_login(self, request):
        # Set up the Google OAuth2.0 flow
        flow = Flow.from_client_secrets_file(
            f'{settings.ROOT_DIR}/backend/client_secret.json',
            scopes=['openid', 'profile', 'email'],
            redirect_uri=request.build_absolute_uri('/users/google-callback/'),
        )

        authorization_url, state = flow.authorization_url(prompt='consent')
        # Store the state so the callback can verify the response.
        request.session['oauth_state'] = state
        return redirect(authorization_url)

    @action(detail=False, methods=['get'], url_path='google-callback')
    def google_callback(self, request):  # pragma: no cover
        # Get the state from the session to verify the response.
        state = request.session.get('oauth_state')

        flow = Flow.from_client_secrets_file(
            f'{settings.ROOT_DIR}/backend/client_secret.json',
            scopes=None,
            redirect_uri=request.build_absolute_uri('/users/google-callback/'),
        )

        # Use the authorization response to get tokens
        flow.fetch_token(authorization_response=request.build_absolute_uri(), state=state)

        # Use the id_token to get user information
        token = flow.credentials.id_token
        request_google_oauth = requests.Request()
        id_info = id_token.verify_oauth2_token(
            token,
            request_google_oauth,
        )

        user = authenticate(request=request, id_info=id_info)

        if user:
            if user.is_active:
                login(request, user)
                redirect_to = settings.REDIRECT_URL
                url_is_safe = url_has_allowed_host_and_scheme(
                    url=redirect_to,
                    allowed_hosts=[request.get_host()],
                    require_https=request.is_secure(),
                )
                redirect_to = redirect_to if url_is_safe else '/'
                return redirect(redirect_to)
            else:
                resp = {'title': 'Permission Denied', 'detail': 'User is not active !'}
                return Response(resp, status=403)
        else:
            resp = {'title': 'Permission Denied', 'detail': 'User does not exist !'}
            return Response(resp, status=403)

    @action(detail=False, methods=['get'], url_path='google-logout')
    def google_logout(self, request):
        logout(request)
        return redirect('/')


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
