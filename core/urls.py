from django.urls import path

from .views import (
    EmailVerificationView,
    OrderDetail,
    OrderList,
    ProductList,
    ProductRetrieveUpdateDestroyAPIView,
    ProfileDetail,
    health,
    payment_webhook,
    signup,
)

urlpatterns = [
    path("health/", health),
    path("signup/", signup),
    path(
        "verify-email/<str:token>/",
        EmailVerificationView.as_view(),
        name="email-verify",
    ),
    path("products/", ProductList.as_view()),
    path("products/<int:pk>", ProductRetrieveUpdateDestroyAPIView.as_view()),
    path("orders/", OrderList.as_view()),
    path("profile/", ProfileDetail.as_view()),
    path("orders/<int:pk>/", OrderDetail.as_view()),
    path("payment-webhook/", payment_webhook),
]
