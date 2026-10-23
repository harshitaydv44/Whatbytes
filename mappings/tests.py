from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from patients.models import Patient, Doctor
from mappings.models import PatientDoctorMapping


class MappingTests(APITestCase):
    def setUp(self):
        # Users
        self.user1 = User.objects.create_user(
            username="user1@example.com",
            email="user1@example.com",
            password="UserPassword123!",
            first_name="User One"
        )
        self.user2 = User.objects.create_user(
            username="user2@example.com",
            email="user2@example.com",
            password="UserPassword123!",
            first_name="User Two"
        )

        # Patients
        self.patient1 = Patient.objects.create(
            user=self.user1,
            name="Alice Walker",
            age=34,
            gender="Female",
            phone="1234567890",
            address="123 Medical Way"
        )
        self.patient2 = Patient.objects.create(
            user=self.user2,
            name="Bob Smith",
            age=45,
            gender="Male",
            phone="0987654321",
            address="456 Health Blvd"
        )

        # Doctors
        self.doctor1 = Doctor.objects.create(
            name="Dr. Gregory House",
            specialization="Diagnostics",
            phone="5551234567",
            email="house@princetonplainsboro.com"
        )
        self.doctor2 = Doctor.objects.create(
            name="Dr. James Wilson",
            specialization="Oncology",
            phone="5559876543",
            email="wilson@princetonplainsboro.com"
        )

        # Existing mapping for patient1 (owned by user1)
        self.mapping1 = PatientDoctorMapping.objects.create(
            patient=self.patient1,
            doctor=self.doctor1
        )

        # Existing mapping for patient2 (owned by user2)
        self.mapping2 = PatientDoctorMapping.objects.create(
            patient=self.patient2,
            doctor=self.doctor2
        )

        self.mappings_url = reverse("mapping-list-create")

    def test_mappings_unauthenticated_access_denied(self):
        """Unauthenticated requests to mappings endpoints must return 401."""
        response = self.client.get(self.mappings_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_mappings_scoped_to_user(self):
        """Listing mappings returns only mappings for patients owned by the user."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.mappings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.mapping1.id)
        self.assertEqual(response.data[0]["patient"], self.patient1.id)

    def test_create_mapping_success(self):
        """User can assign another doctor to their owned patient."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "patient": self.patient1.id,
            "doctor": self.doctor2.id
        }
        response = self.client.post(self.mappings_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["patient"], self.patient1.id)
        self.assertEqual(response.data["doctor"], self.doctor2.id)

        self.assertTrue(
            PatientDoctorMapping.objects.filter(
                patient=self.patient1,
                doctor=self.doctor2
            ).exists()
        )

    def test_create_mapping_duplicate_rejection(self):
        """Assigning the same doctor to the same patient again must be rejected."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "patient": self.patient1.id,
            "doctor": self.doctor1.id  # Already assigned in setUp
        }
        response = self.client.post(self.mappings_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already assigned", str(response.data))

    def test_create_mapping_for_another_users_patient_denied(self):
        """User cannot assign a doctor to another user's patient (HTTP 403)."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "patient": self.patient2.id,  # Owned by user2
            "doctor": self.doctor1.id
        }
        response = self.client.post(self.mappings_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_patient_specific_mappings_success(self):
        """User can retrieve all mappings for their patient via explicit route."""
        self.client.force_authenticate(user=self.user1)
        patient_mappings_url = reverse(
            "patient-mappings",
            kwargs={"patient_id": self.patient1.id}
        )
        response = self.client.get(patient_mappings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["doctor"], self.doctor1.id)

    def test_get_patient_specific_mappings_for_other_user_denied(self):
        """User cannot retrieve doctor mappings for another user's patient."""
        self.client.force_authenticate(user=self.user1)
        other_patient_mappings_url = reverse(
            "patient-mappings",
            kwargs={"patient_id": self.patient2.id}
        )
        response = self.client.get(other_patient_mappings_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_patient_specific_mappings_nonexistent_patient(self):
        """Querying mappings for a nonexistent patient returns 404."""
        self.client.force_authenticate(user=self.user1)
        not_found_url = reverse(
            "patient-mappings",
            kwargs={"patient_id": 99999}
        )
        response = self.client.get(not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_mapping_detail_by_mapping_id(self):
        """User can retrieve a specific mapping by mapping ID."""
        self.client.force_authenticate(user=self.user1)
        detail_url = reverse(
            "mapping-detail",
            kwargs={"pk": self.mapping1.id}
        )
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.mapping1.id)

    def test_get_mapping_detail_for_other_user_denied(self):
        """User cannot access another user's mapping by mapping ID."""
        self.client.force_authenticate(user=self.user1)
        other_detail_url = reverse(
            "mapping-detail",
            kwargs={"pk": self.mapping2.id}
        )
        response = self.client.get(other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_mapping_success(self):
        """User can delete an assignment mapping for their own patient."""
        self.client.force_authenticate(user=self.user1)
        delete_url = reverse(
            "mapping-detail",
            kwargs={"pk": self.mapping1.id}
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertFalse(
            PatientDoctorMapping.objects.filter(pk=self.mapping1.id).exists()
        )

    def test_delete_mapping_for_other_user_denied(self):
        """User cannot delete another user's mapping."""
        self.client.force_authenticate(user=self.user1)
        other_delete_url = reverse(
            "mapping-detail",
            kwargs={"pk": self.mapping2.id}
        )
        response = self.client.delete(other_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            PatientDoctorMapping.objects.filter(pk=self.mapping2.id).exists()
        )
