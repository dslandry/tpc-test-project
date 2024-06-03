from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import Order, Product
from tests.factories.core_factories import (
    OrderFactory,
    ProductFactory,
    ProfileFactory,
    UserFactory,
)


class TestOrder(APITestCase):

    def setUp(self):
        self.profile = ProfileFactory()
        self.client.login(username=self.profile.user.username, password="password")
        self.product = ProductFactory(stock=5)
        self.order = OrderFactory(client=self.profile, product=self.product)

    def test_list_orders_for_client(self):
        response = self.client.get("/api/orders/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_list_orders_empty_for_inappropriate_client(self):
        user = UserFactory()
        self.client.login(username=user.username, password="password")
        response = self.client.get("/api/orders/", format="json")
        assert response.status_code == 200
        assert len(response.data["results"]) == 0

    def test_create_order_on_product_with_sufficient_quantity(self):
        Order.objects.all().delete()
        data = {
            "product": self.product.id,
            "quantity": 3,
        }
        response = self.client.post("/api/orders/", data, format="json")
        assert response.status_code == 201
        assert Order.objects.count() == 1
        self.product.refresh_from_db()
        assert self.product.stock == 2

    def test_create_order_fails_on_product_with_insufficient_quantity(self):
        Order.objects.all().delete()
        data = {
            "product": self.product.id,
            "quantity": 6,
        }
        response = self.client.post("/api/orders/", data, format="json")
        assert response.status_code == 400
        assert Order.objects.count() == 0
        self.product.refresh_from_db()
        assert self.product.stock == 5

    def test_webhook_updates_pending_order_on_payment_successful(self):
        data = {
            "order_id": self.order.id,
            "payment_status": "confirmed",
        }
        response = self.client.post("/api/payment-webhook/", data, format="json")
        assert response.status_code == 200
        self.order.refresh_from_db()
        assert self.order.status == "confirmed"

    def test_webhook_updates_pending_order_on_payment_failed(self):
        self.order.refresh_from_db()
        data = {
            "order_id": self.order.id,
            "payment_status": "failed",
        }
        response = self.client.post("/api/payment-webhook/", data, format="json")
        assert response.status_code == 200
        self.order.refresh_from_db()
        assert self.order.status == "pending"

    def test_webhook_updates_wrong_order_id(self):
        data = {
            "order_id": -1,
            "payment_status": "failed",
        }
        response = self.client.post("/api/payment-webhook/", data, format="json")
        assert response.status_code == 404
