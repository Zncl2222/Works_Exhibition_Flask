from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from google.auth.transport import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

from .mail import send_validation_mail
from .models import User


class OAuthAuthenticationBackend(ModelBackend):
    """
    Authentication backend to allow user use Google to login.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        state = kwargs.get('oauth_state')
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

        user = self.get_google_oauth_user(id_info)
        return user

    def get_google_oauth_user(self, id_info):
        data = {
            'first_name': id_info['given_name'],
            'last_name': id_info['family_name'],
            'email': id_info['email'],
        }
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User.objects.create(**data)
            send_validation_mail(email=data['email'])

        return user
