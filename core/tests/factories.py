import factory
from django.contrib.auth.models import User

from .models import Order, Product, Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    address = factory.Faker("address")
    phone_number = factory.Faker("phone_number")
    date_of_birth = factory.Faker("date_of_birth")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = factory.Faker("text")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker("pyint", min_value=0, max_value=1000)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    status = factory.Faker(
        "random_element", elements=["pending", "confirmed", "shipped", "delivered"]
    )
