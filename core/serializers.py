from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password,
)
from django.db import transaction
from django.db.models import F, Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.exceptions import UserEmailConflict

from .models import Order, Product, Profile

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def get_value(self, dictionary):
        return dictionary

    def validate(self, data):
        data["email"] = data["email"].lower()
        self._validate_email_available(data["email"])
        self._validate_password(data["password"])
        return data

    def _validate_email_available(self, email):
        if User.objects.filter(Q(username=email) | Q(email=email)).exists():
            raise UserEmailConflict(email)

    def _validate_password(self, password):
        validators = get_default_password_validators()
        validate_password(
            password,
            password_validators=validators,
        )


class SignUpSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "user",
            "phone_number",
            "date_of_birth",
            "address",
            "phone_number",
        ]

    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except ValidationError as e:
            e.detail.update(e.detail.pop("user", {}))
            raise ValidationError(e.detail)

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        with transaction.atomic():
            username = user_data["email"]
            user = User.objects.create_user(username, **user_data)
            profile = Profile.objects.create(user=user, **validated_data)
        return profile
