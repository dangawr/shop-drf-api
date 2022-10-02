from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class ModelTests(APITestCase):

    def test_create_user(self):
        payload = {
            'email': 'example@example.com',
            'name': 'test_name',
            'password': 'pass123',
        }
        user = get_user_model().objects.create_user(**payload)

        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_normalize_email(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, name='testname', password='test123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', name='testname', password='test123')
