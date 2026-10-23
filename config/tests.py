from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class HomepageAndRoutingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username="tester@example.com",
            email="tester@example.com",
            password="SecureTestPassword123!"
        )

    def test_homepage_status_200(self):
        """Root route / must return HTTP 200 and render the healthcare dashboard."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Healthcare Management System", content)
        self.assertIn("Backend API Dashboard", content)
        self.assertIn("Authentication", content)
        self.assertIn("Patient Management", content)
        self.assertIn("Doctor Management", content)
        self.assertIn("Patient-Doctor Mappings", content)
        self.assertIn("Django Administration", content)

    def test_url_resolutions(self):
        """Verify URL reversing and resolution match expected endpoint paths."""
        self.assertEqual(reverse("home"), "/")
        self.assertEqual(resolve("/").view_name, "home")

        self.assertEqual(reverse("register"), "/api/auth/register/")
        self.assertEqual(resolve("/api/auth/register/").view_name, "register")

        self.assertEqual(reverse("login"), "/api/auth/login/")
        self.assertEqual(resolve("/api/auth/login/").view_name, "login")

        self.assertEqual(reverse("patient-list"), "/api/patients/")
        self.assertEqual(resolve("/api/patients/").view_name, "patient-list")

        self.assertEqual(reverse("doctor-list"), "/api/doctors/")
        self.assertEqual(resolve("/api/doctors/").view_name, "doctor-list")

        self.assertEqual(reverse("mapping-list-create"), "/api/mappings/")
        self.assertEqual(resolve("/api/mappings/").view_name, "mapping-list-create")

        self.assertEqual(
            reverse("mapping-detail", kwargs={"pk": 1}),
            "/api/mappings/1/"
        )
        self.assertEqual(resolve("/api/mappings/1/").view_name, "mapping-detail")

        self.assertEqual(
            reverse("patient-mappings", kwargs={"patient_id": 42}),
            "/api/mappings/patient/42/"
        )
        self.assertEqual(
            resolve("/api/mappings/patient/42/").view_name,
            "patient-mappings"
        )

    def test_jwt_protected_api_access(self):
        """Verify JWT header 'Authorization: Bearer <token>' grants access to protected endpoints."""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # Unauthenticated request fails
        unauth_res = self.api_client.get(reverse("patient-list"))
        self.assertEqual(unauth_res.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated with Bearer token succeeds
        self.api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        auth_res = self.api_client.get(reverse("patient-list"))
        self.assertEqual(auth_res.status_code, status.HTTP_200_OK)

        # Invalid token fails
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token-string")
        invalid_res = self.api_client.get(reverse("patient-list"))
        self.assertEqual(invalid_res.status_code, status.HTTP_401_UNAUTHORIZED)
