from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories.core_factories import OrderFactory, ProductFactory, UserFactory


class APITests(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password="password")
        self.product = ProductFactory()
        self.order = OrderFactory(user=self.user, product=self.product)

    def test_create_product(self):
        data = {
            "name": "New Product",
            "description": "New product description",
            "price": "15.00",
            "stock": 100,
        }
        response = self.client.post("/api/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_product_list(self):
        response = self.client.get("/api/products/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_order(self):
        data = {
            "user": self.user.id,
            "product": self.product.id,
            "quantity": 1,
            "status": "pending",
        }
        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_list(self):
        response = self.client.get("/api/orders/", format="json")
        assert response.status_code == 200
        assert len(response.data) > 1

    def test_get_profile_list(self):
        response = self.client.get("/api/profile/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
