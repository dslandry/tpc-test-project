from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, Product, Profile
from .serializers import OrderSerializer, ProductSerializer, ProfileSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


@api_view(["POST"])
def payment_webhook(request):
    order_id = request.data.get("order_id")
    payment_status = request.data.get("payment_status")

    try:
        order = Order.objects.get(id=order_id)
        if payment_status == "confirmed":
            order.status = "confirmed"
            order.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "failed", "error": "Invalid payment status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except Order.DoesNotExist:
        return Response(
            {"status": "failed", "error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
