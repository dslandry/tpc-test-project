from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import OrderFactory, ProductFactory, ProfileFactory, UserFactory


class APITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password="password")
        self.product = ProductFactory()
        self.order = OrderFactory(user=self.user, product=self.product)

    def test_create_product(self):
        url = reverse("product-list")
        data = {
            "name": "New Product",
            "description": "New product description",
            "price": "15.00",
            "stock": 100,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_list(self):
        url = reverse("product-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_order(self):
        url = reverse("order-list")
        data = {
            "user": self.user.id,
            "product": self.product.id,
            "quantity": 1,
            "status": "pending",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_list(self):
        url = reverse("order-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_profile(self):
        url = reverse("profile-list")
        user = UserFactory()
        data = {
            "user": user.id,
            "address": "456 Elm St",
            "phone_number": "1234567890",
            "date_of_birth": "1990-01-01",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_profile_list(self):
        url = reverse("profile-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
