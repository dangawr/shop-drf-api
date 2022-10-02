from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model


class PublicUser(APITestCase):

    def test_user_create_endpoint(self):
        payload = {
            'email': 'test@example.com',
            'name': 'testname',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('user:create'), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertEqual(user.name, payload['name'])
        self.assertNotIn('password', response.data)

    def test_user_create_wrong_passwords(self):
        payload = {
            'email': 'test@example.com',
            'name': 'testname',
            'password': 'testpass123',
            'password2': 'test'
        }

        with self.assertRaises(ValueError):
            self.client.post(reverse('user:create'), payload)
