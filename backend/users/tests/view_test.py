from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import User, EmailValidationToken


class EmailValidationViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('email_validation')
        self.email = 'test@example.com'
        self.user = User.objects.create(email=self.email)

    def test_email_validation_success(self):
        data = {'email': self.email}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'detail': 'Validation email sent.'})

        email_validation_token = EmailValidationToken.objects.filter(user=self.user).first()
        self.assertIsNotNone(email_validation_token)

    def test_email_validation_user_not_found(self):
        data = {'email': 'not_found@example.com'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'User not found.'})

    def test_email_validation_email_already_validated(self):
        self.user.email_validated = True
        self.user.save()

        data = {'email': self.email}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
