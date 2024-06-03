import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories.core_factories import (
    OrderFactory,
    ProductFactory,
    ProfileFactory,
    UserFactory,
)


class ProductAdminTestCase(APITestCase):

    def setUp(self):
        self.profile = ProfileFactory(user__is_staff=True)
        self.client.login(username=self.profile.user.username, password="password")
        self.product = ProductFactory()

    def test_get_product_as_admin(self):
        response = self.client.get("/api/products/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_get_product_as_non_admin(self):
        user = UserFactory()
        self.client.login(username=user.username, password="password")
        response = self.client.get("/api/products/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_create_product_successful_as_admin(self):
        response = self.client.post(
            "/api/products/",
            data={
                "name": "Test Product",
                "description": "A detailed description of the product",
                "price": 10.15,
            },
            format="json",
        )
        assert response.status_code == 201
        assert response.data["name"] == "Test Product"
        assert response.data["price"] == "10.15"

    def test_create_product_list_fail_as_non_admin(self):
        user = UserFactory()
        self.client.login(username=user.username, password="password")
        response = self.client.post(
            "/api/products/",
            data={
                "name": "Test Product",
                "description": "A detailed description of the product",
                "price": 10.15,
            },
            format="json",
        )
        assert response.status_code == 403
        self.client.logout()
