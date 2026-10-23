from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        ).select_related(
            "patient", "doctor"
        )

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]

        if patient.user_id != self.request.user.id:
            raise PermissionDenied(
                "You cannot assign a doctor to another user's patient."
            )

        serializer.save()


class PatientMappingView(generics.GenericAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        patient = get_object_or_404(
            Patient,
            pk=pk,
            user=request.user
        )

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related("patient", "doctor")

        serializer = self.get_serializer(
            mappings,
            many=True
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = get_object_or_404(
            PatientDoctorMapping.objects.select_related("patient"),
            pk=pk
        )

        if mapping.patient.user_id != request.user.id:
            raise PermissionDenied(
                "You cannot remove another user's patient mapping."
            )

        mapping.delete()

        return Response(
            {"message": "Doctor assignment removed successfully."},
            status=status.HTTP_200_OK
        )