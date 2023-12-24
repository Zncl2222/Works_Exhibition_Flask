from django.contrib.auth.backends import ModelBackend
from .models import User


class OAuthAuthenticationBackend(ModelBackend):
    """
    Authentication backend to allow authenticating users against a
    Microsoft ADFS server with an authorization code.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('id_info'):
            user = self.get_google_oauth_user(kwargs.get('id_info'))
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

        return user
