from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer
from .permissions import IsPatientOwner


class PatientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing patient records.
    Restricted to authenticated users and scoped strictly to patients owned by the user.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOwner]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Patient.objects.none()
        return Patient.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing doctor records.
    Accessible to authenticated users for directory and assignment management.
    """
    queryset = Doctor.objects.all().order_by("-created_at")
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
