from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, permissions, serializers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.mail import EmailTemplates, mail_notify

from .models import Order, Product, Profile
from .serializers import (
    OrderSerializer,
    ProductSerializer,
    ProfileSerializer,
    SignUpSerializer,
)


class ProductList(generics.ListCreateAPIView):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = permissions.IsAdminUser

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.IsAuthenticatedOrReadOnly()]
        return [permissions.IsAdminUser()]


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(client__user__id=self.request.user.pk)


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


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ["GET"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def payment_webhook(request):
    order_id = request.data.get("order_id")
    payment_status = request.data.get("payment_status")

    try:
        order = Order.objects.get(id=order_id)
        if payment_status == "confirmed":
            order.status = "confirmed"
            order.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        elif payment_status != "failed":
            return Response(
                {"status": "failed", "error": "Invalid payment status"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response({"status": "success"}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response(
            {"status": "failed", "error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
@ensure_csrf_cookie
@permission_classes([permissions.AllowAny])
def signup(request):

    serializer = SignUpSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
    except ValidationError as e:
        return Response(e.get_full_details(), status=status.HTTP_400_BAD_REQUEST)
    else:
        mail_notify(profile.user, EmailTemplates.CONFIRM_EMAIL)

    return Response(status=status.HTTP_201_CREATED)


@permission_classes([permissions.AllowAny])
class EmailVerificationView(APIView):
    def get(self, request, token):
        user_profile = Profile.objects.filter(verification_token=token).first()
        if user_profile:
            user_profile.confirmed_email = True
            user_profile.save()

            return redirect("https://yourdomain.com/email-verified/")
        else:
            return Response(
                {"error": "Invalid verification token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
