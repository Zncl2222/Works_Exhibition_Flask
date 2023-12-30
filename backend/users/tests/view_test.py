from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import EmailValidationToken, User


class RegisterViewTest(APITestCase):
    url = reverse('register')
    data = {
        'username': 'test',
        'password': '1234',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
    }

    def test_register_and_email_validation_success(self):
        resp = self.client.post(self.url, self.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = User.objects.filter(username='test').first()
        email_validation_token = EmailValidationToken.objects.filter(user=user).first()
        self.assertIsNotNone(email_validation_token)

        resp = self.client.post(
            reverse('email_validation_confirm'),
            {'token': email_validation_token.token},
        )
        assert resp.status_code == status.HTTP_302_FOUND

        # Token has alredy verified.
        resp = self.client.post(
            reverse('email_validation_confirm'),
            {'token': email_validation_token.token},
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST


class GoogleOAuthLoginViewTest(APITestCase):
    def test_google_oauth_login(self):
        # Simulate a POST request to the view
        resp = self.client.get('/users/google-login/')
        assert resp.status_code == status.HTTP_302_FOUND

    def test_google_oauth_logout(self):
        resp = self.client.get('/users/google-logout/')
        assert resp.status_code == status.HTTP_302_FOUND

    # TODO: Google Oauth Callback test
