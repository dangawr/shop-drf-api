from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


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

    def test_create_token_for_user(self):
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        get_user_model().objects.create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(reverse('user:token'), payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        get_user_model().objects.create_user(email='test@example.com', name='test', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(reverse('user:token'), payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(reverse('user:token'), payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(reverse('user:token'), payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class RegisteredUser(APITestCase):

    def setUp(self) -> None:
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        self.user = get_user_model().objects.create_user(**user_details)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        response = self.client.get(reverse('user:me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_change_password(self):
        updated_data = {
            'password': 'test-user-password123',
            'new_password': 'updated',
            'repeat_new_password': 'updated',
        }
        response = self.client.patch(reverse('user:me'), updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(updated_data['new_password']))

    def test_change_wrong_password(self):
        updated_data = {
            'password': 'wrong_password',
            'new_password': 'updated',
            'repeat_new_password': 'updated',
        }

        with self.assertRaises(ValueError):
            self.client.patch(reverse('user:me'), updated_data)

    def test_change_wrong_repeat_password(self):
        updated_data = {
            'password': 'test-user-password123',
            'new_password': 'updated',
            'repeat_new_password': 'wrong_repeat',
        }

        with self.assertRaises(ValueError):
            self.client.patch(reverse('user:me'), updated_data)

    def test_logout_user(self):
        Token.objects.get_or_create(user=self.user)
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
