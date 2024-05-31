from django.urls import path

from .views import OrderDetail, OrderList, ProductList, ProfileDetail, payment_webhook

urlpatterns = [
    path("products/", ProductList.as_view(), name="product-list"),
    path("orders/", OrderList.as_view(), name="order-list"),
    path("profile/", ProfileDetail.as_view(), name="profile-detail"),
    path("orders/<int:pk>/", OrderDetail.as_view(), name="order-detail"),
    path("payment-webhook/", payment_webhook, name="payment-webhook"),
]
