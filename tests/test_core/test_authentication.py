import uuid

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.models import Profile
from tests.factories.core_factories import ProfileFactory


class AuthenticationTestCase(TestCase):
    def setUp(self):

        self.sign_up_url = "/api/signup/"
        self.email_verification_url = "/api/verify-email/"

    def test_sign_up_successful(self):
        response = self.client.post(
            self.sign_up_url,
            {
                "email": "user@test.com",
                "password": "#password2024",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1994-07-12",
                "address": "2 rue de Paris",
                "phone_number": "+33 6 22 22 22 22",
            },
        )

        assert response.status_code == 201
        assert Profile.objects.count() == 1
        assert Profile.objects.first().user.email == "user@test.com"

    def test_sign_up_unsuccessful_with_already_used_email(self):
        ProfileFactory(user__email="user@test.com")
        response = self.client.post(
            self.sign_up_url,
            {
                "email": "user@test.com",
                "password": "#password2024",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1994-07-12",
                "address": "2 rue de Paris",
                "phone_number": "+33 6 22 22 22 22",
            },
        )
        assert response.status_code == 409

    def test_sign_up_unsuccessful_with_short_password(self):
        response = self.client.post(
            self.sign_up_url,
            {
                "email": "user@test.com",
                "password": "a",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1994-07-12",
                "address": "2 rue de Paris",
                "phone_number": "+33 6 22 22 22 22",
            },
        )

        assert response.status_code == 400
        response.data["non_field_errors"][0]["code"] = "password_too_short"

    def test_email_verification(self):
        profile = ProfileFactory(user__email="user@test.com")
        assert profile.confirmed_email == False

        response = self.client.get(f"/api/verify-email/{profile.verification_token}/")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        profile.refresh_from_db()
        assert profile.confirmed_email
        assert response["Location"] == "https://yourdomain.com/email-verified/"

    def test_invalid_verification_token(self):
        ProfileFactory(user__email="user@test.com")
        # Make GET request with invalid token
        response = self.client.get(f"/api/verify-email/{uuid.uuid4()}/")

        # Ensure status code is 400 (Bad Request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
