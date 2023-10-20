import pytest
from rest_framework import status
from users.models import User
from rest_framework.test import APITestCase


@pytest.mark.sgsim
class ViewSetsTests(APITestCase):
    def setUp(self):
        self.customer = User.objects.create(
            username='test',
            email='test@zweb.com',
            is_staff=True,
            is_active=True,
        )
        self.client.force_authenticate(user=self.customer)

    def test_email_failed_sgsim(self):
        data = {
            'realizations_number': 10,
            'cov_model': 'Gaussian',
            'kernel': 'Python',
            'bandwidth': 35,
            'bandwidth_step': 1,
            'x_size': 150,
            'y_size': 0,
            'randomseed': 12151,
            'krige_range': 17.32,
            'krige_sill': 1,
        }
        resp = self.client.post('/api/sgsim/', data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_email_failed_sgsim_list(self):
        resp = self.client.get('/api/sgsimlist/')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_sgsim(self):
        data = {
            'realizations_number': 10,
            'cov_model': 'Gaussian',
            'kernel': 'Python',
            'bandwidth': 35,
            'bandwidth_step': 1,
            'x_size': 150,
            'y_size': 0,
            'randomseed': 12151,
            'krige_range': 17.32,
            'krige_sill': 1,
        }
        self.customer.email_validated = True
        self.customer.save()
        resp = self.client.post('/api/sgsim/', data)
        assert resp.status_code == status.HTTP_201_CREATED

    def test_sgsim_list(self):
        self.customer.email_validated = True
        self.customer.save()
        resp = self.client.get('/api/sgsimlist/')
        assert resp.status_code == status.HTTP_200_OK
