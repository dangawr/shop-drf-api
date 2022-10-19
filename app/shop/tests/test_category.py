from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Category, Product
from decimal import Decimal


class PublicUserTests(APITestCase):

    def test_get_categories(self):
        response = self.client.get(reverse('shop:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_category(self):
        payload = {
            'name': 'test_name_category',
        }
        response = self.client.post(reverse('shop:category-list'), payload)
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

    def test_get_products(self):
        response = self.client.get(reverse('shop:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_create(self):
        payload = {
            'name': 'test_name_category',
        }
        self.user.is_staff = True
        response = self.client.post(reverse('shop:category-list'), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=response.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(category, k), v)

    def test_category_products_counter(self):
        category = Category.objects.create(name='test')
        payload_1 = {
            'name': 'test_name',
            'quantity': 10,
            'price': Decimal('10.99'),
            'description': 'some test description',
        }
        payload_2 = {
            'name': 'test_name2',
            'quantity': 10,
            'price': Decimal('10.99'),
            'description': 'some test description',
        }
        product1 = Product.objects.create(user=self.user, **payload_1)
        product2 = Product.objects.create(user=self.user, **payload_2)
        category.products.add(product1)
        category.products.add(product2)

        response = self.client.get(reverse('shop:category-detail', args=[category.pk]))
        self.assertEqual(response.data['products_count'], 2)
