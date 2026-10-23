from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Patient, Doctor
from .serializers import PatientSerializer, DoctorSerializer
from .permissions import IsPatientOwner


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsPatientOwner]

    def get_queryset(self):
        return Patient.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by("-created_at")
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]