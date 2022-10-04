from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Product
from decimal import Decimal


class PublicUserTests(APITestCase):

    def test_get_products(self):
        response = self.client.get(reverse('shop:product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_product(self):
        payload = {
            'name': 'test_name',
            'quantity': 10,
            'price': Decimal('10.99'),
            'description': 'some test description',
        }
        response = self.client.post(reverse('shop:product-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserTests(APITestCase):

    def setUp(self) -> None:
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        self.user = get_user_model().objects.create_user(**user_details)
        self.client.force_authenticate(user=self.user)

    def test_product_create(self):
        payload = {
            'name': 'test_name',
            'quantity': 10,
            'price': Decimal('10.99'),
            'description': 'some test description',
        }
        response = self.client.post(reverse('shop:product-list'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)
        self.assertTrue(response.data['is_available'])

    def test_update_is_available(self):
        payload = {
            'name': 'test_nameeee',
            'quantity': 10,
            'price': Decimal('10.99'),
            'description': 'some test description',
        }
        product = Product.objects.create(user=self.user, **payload)

        updated_quantity = {'quantity': 0}
        response = self.client.patch(reverse('shop:product-detail', args=[product.pk]), updated_quantity)
        self.assertFalse(response.data['is_available'])

