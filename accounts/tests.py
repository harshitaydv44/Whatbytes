from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_password = "SecurePassword123!"
        self.user_email = "testuser@example.com"
        self.user_name = "Test User"

        self.user = User.objects.create_user(
            username=self.user_email,
            email=self.user_email,
            password=self.user_password,
            first_name=self.user_name
        )

    def test_registration_success(self):
        """Verify successful user registration with hashed password and without exposing password in response."""
        data = {
            "name": "New Registered User",
            "email": "newuser@example.com",
            "password": "NewUserPassword123!"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Registered User")
        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertNotIn("password", response.data)

        new_user = User.objects.filter(email="newuser@example.com").first()
        self.assertIsNotNone(new_user)
        self.assertTrue(new_user.check_password("NewUserPassword123!"))

    def test_registration_duplicate_email_rejection(self):
        """Verify registration is rejected when an account with the same email already exists."""
        data = {
            "name": "Duplicate User",
            "email": self.user_email.upper(),  # Test case-insensitivity
            "password": "AnotherPassword123!"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_registration_short_password(self):
        """Verify registration rejects passwords shorter than 8 characters."""
        data = {
            "name": "Short Pass User",
            "email": "shortpass@example.com",
            "password": "12345"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        """Verify valid credentials return JWT access and refresh tokens."""
        data = {
            "email": self.user_email,
            "password": self.user_password
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("message", response.data)

    def test_login_case_insensitive_email(self):
        """Verify login succeeds even when email case differs from registered case."""
        data = {
            "email": "TESTUSER@EXAMPLE.COM",
            "password": self.user_password
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_invalid_password(self):
        """Verify login fails with wrong password."""
        data = {
            "email": self.user_email,
            "password": "WrongPassword!"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_login_nonexistent_user(self):
        """Verify login fails for unregistered email."""
        data = {
            "email": "nonexistent@example.com",
            "password": "SomePassword123!"
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_inactive_user(self):
        """Verify inactive users cannot log in."""
        self.user.is_active = False
        self.user.save()

        data = {
            "email": self.user_email,
            "password": self.user_password
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)
