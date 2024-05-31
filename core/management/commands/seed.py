import random
from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import Order, Product, Profile


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create users
        user1 = User.objects.create_user(
            username="user1", password="password1", email="user1@example.com"
        )
        user2 = User.objects.create_user(
            username="user2", password="password2", email="user2@example.com"
        )
        user3 = User.objects.create_user(
            username="user3", password="password3", email="user3@example.com"
        )

        # Create profiles
        Profile.objects.create(
            user=user1,
            address="123 Main St",
            phone_number="1234567890",
            date_of_birth=date(1990, 1, 1),
        )
        Profile.objects.create(
            user=user2,
            address="456 Elm St",
            phone_number="0987654321",
            date_of_birth=date(1992, 2, 2),
        )
        Profile.objects.create(
            user=user3,
            address="789 Oak St",
            phone_number="1122334455",
            date_of_birth=date(1994, 3, 3),
        )

        # Create products
        product1 = Product.objects.create(
            name="Product 1",
            description="Description for product 1",
            price=10.00,
            stock=100,
        )
        product2 = Product.objects.create(
            name="Product 2",
            description="Description for product 2",
            price=20.00,
            stock=200,
        )
        product3 = Product.objects.create(
            name="Product 3",
            description="Description for product 3",
            price=30.00,
            stock=300,
        )

        # Create orders
        Order.objects.create(user=user1, product=product1, quantity=2, status="pending")
        Order.objects.create(
            user=user2, product=product2, quantity=1, status="confirmed"
        )
        Order.objects.create(user=user3, product=product3, quantity=3, status="shipped")

        self.stdout.write(self.style.SUCCESS("Data seeded successfully!"))
