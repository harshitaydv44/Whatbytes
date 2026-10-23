from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from patients.models import Patient, Doctor


class PatientAndDoctorTests(APITestCase):
    def setUp(self):
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

        self.doctor = Doctor.objects.create(
            name="Dr. Gregory House",
            specialization="Diagnostics",
            phone="5551234567",
            email="house@princetonplainsboro.com"
        )

        self.patients_url = reverse("patient-list")
        self.doctors_url = reverse("doctor-list")

    # --- Patient Tests ---

    def test_patients_unauthenticated_access_denied(self):
        """Unauthenticated requests to patients endpoints must return 401."""
        response = self.client.get(self.patients_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_patients_scoped_to_authenticated_user(self):
        """A user should only see their own patients in the list view."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.patients_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.patient1.id)
        self.assertEqual(response.data[0]["name"], self.patient1.name)

    def test_create_patient_success(self):
        """A user can successfully create a patient associated with themselves."""
        self.client.force_authenticate(user=self.user1)
        data = {
            "name": "Charlie Brown",
            "age": 28,
            "gender": "Male",
            "phone": "9998887777",
            "address": "789 Pine Lane"
        }
        response = self.client.post(self.patients_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Charlie Brown")

        created_patient = Patient.objects.get(pk=response.data["id"])
        self.assertEqual(created_patient.user, self.user1)

    def test_patient_age_validation(self):
        """Patient age must be between 0 and 120."""
        self.client.force_authenticate(user=self.user1)

        # Invalid: Negative age
        response = self.client.post(self.patients_url, {
            "name": "Invalid Patient",
            "age": -1,
            "gender": "Other",
            "phone": "1234567890",
            "address": "Nowhere"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)

        # Invalid: Age > 120
        response = self.client.post(self.patients_url, {
            "name": "Invalid Patient",
            "age": 125,
            "gender": "Other",
            "phone": "1234567890",
            "address": "Nowhere"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)

        # Valid boundary: Age 0 (infant)
        response = self.client.post(self.patients_url, {
            "name": "Infant Patient",
            "age": 0,
            "gender": "Female",
            "phone": "1234567890",
            "address": "Nowhere"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_ownership_retrieve_restriction(self):
        """A user cannot retrieve another user's patient."""
        self.client.force_authenticate(user=self.user1)
        other_patient_url = reverse("patient-detail", kwargs={"pk": self.patient2.id})
        response = self.client.get(other_patient_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_ownership_update_restriction(self):
        """A user cannot update another user's patient."""
        self.client.force_authenticate(user=self.user1)
        other_patient_url = reverse("patient-detail", kwargs={"pk": self.patient2.id})
        response = self.client.patch(other_patient_url, {"name": "Hacked Name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify database record unchanged
        self.patient2.refresh_from_db()
        self.assertEqual(self.patient2.name, "Bob Smith")

    def test_patient_ownership_delete_restriction(self):
        """A user cannot delete another user's patient."""
        self.client.force_authenticate(user=self.user1)
        other_patient_url = reverse("patient-detail", kwargs={"pk": self.patient2.id})
        response = self.client.delete(other_patient_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify database record still exists
        self.assertTrue(Patient.objects.filter(pk=self.patient2.id).exists())

    def test_patient_crud_lifecycle_for_owner(self):
        """Patient owner can retrieve, update, and delete their own patient."""
        self.client.force_authenticate(user=self.user1)
        patient_url = reverse("patient-detail", kwargs={"pk": self.patient1.id})

        # Retrieve
        get_res = self.client.get(patient_url)
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data["name"], "Alice Walker")

        # Partial update
        patch_res = self.client.patch(patient_url, {"phone": "1112223333"}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_res.data["phone"], "1112223333")

        # Full update
        put_res = self.client.put(patient_url, {
            "name": "Alice Walker Updated",
            "age": 35,
            "gender": "Female",
            "phone": "1112223333",
            "address": "New Address 101"
        }, format="json")
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data["name"], "Alice Walker Updated")

        # Delete
        del_res = self.client.delete(patient_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(pk=self.patient1.id).exists())

    # --- Doctor Tests ---

    def test_doctor_unauthenticated_access_denied(self):
        """Unauthenticated access to doctor endpoints must return 401."""
        response = self.client.get(self.doctors_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_doctor_crud_lifecycle(self):
        """Authenticated users can perform CRUD on doctors."""
        self.client.force_authenticate(user=self.user1)

        # List
        list_res = self.client.get(self.doctors_url)
        self.assertEqual(list_res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_res.data), 1)

        # Create
        create_res = self.client.post(self.doctors_url, {
            "name": "Dr. Allison Cameron",
            "specialization": "Immunology",
            "phone": "5559876543",
            "email": "cameron@ppth.org"
        }, format="json")
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        new_doc_id = create_res.data["id"]

        # Retrieve
        doc_detail_url = reverse("doctor-detail", kwargs={"pk": new_doc_id})
        get_res = self.client.get(doc_detail_url)
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data["specialization"], "Immunology")

        # Update
        patch_res = self.client.patch(doc_detail_url, {"specialization": "Diagnostic Medicine"}, format="json")
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_res.data["specialization"], "Diagnostic Medicine")

        # Delete
        del_res = self.client.delete(doc_detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=new_doc_id).exists())

    def test_doctor_duplicate_email_rejection(self):
        """Doctor emails must be unique."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.doctors_url, {
            "name": "Dr. Impostor",
            "specialization": "Neurology",
            "phone": "5550001111",
            "email": self.doctor.email
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
