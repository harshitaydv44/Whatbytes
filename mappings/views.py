from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient


class MappingListCreateView(generics.ListCreateAPIView):
    """
    GET: List all doctor mappings for patients owned by the authenticated user.
         Supports optional query parameter ?patient=<patient_id> to filter by patient.
    POST: Assign a doctor to a patient owned by the authenticated user.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return PatientDoctorMapping.objects.none()

        queryset = PatientDoctorMapping.objects.filter(
            patient__user=user
        ).select_related("patient", "doctor").order_by("-created_at")

        patient_id = self.request.query_params.get("patient") or self.request.query_params.get("patient_id")
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        if patient.user_id != self.request.user.id:
            raise PermissionDenied(
                "You cannot assign a doctor to another user's patient."
            )
        serializer.save()


class MappingDetailView(generics.RetrieveDestroyAPIView):
    """
    GET: Retrieve a single mapping by mapping ID.
    DELETE: Delete a single mapping by mapping ID.
    Only allows access if the mapping belongs to a patient owned by the authenticated user.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PatientDoctorMapping.objects.none()
        return PatientDoctorMapping.objects.select_related("patient", "doctor")

    def get_object(self):
        mapping = get_object_or_404(
            self.get_queryset(),
            pk=self.kwargs.get("pk")
        )
        if mapping.patient.user_id != self.request.user.id:
            raise PermissionDenied(
                "You cannot access another user's patient mapping."
            )
        return mapping

    def delete(self, request, *args, **kwargs):
        mapping = self.get_object()
        mapping.delete()
        return Response(
            {"message": "Doctor assignment removed successfully."},
            status=status.HTTP_200_OK
        )


class PatientMappingsView(generics.GenericAPIView):
    """
    GET: Retrieve all doctor mappings for a specific patient.
    The patient must belong to the authenticated user.
    """
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        patient = Patient.objects.filter(pk=patient_id).first()
        if not patient:
            raise NotFound("Patient not found.")

        if patient.user_id != request.user.id:
            raise PermissionDenied(
                "You cannot view mappings for another user's patient."
            )

        mappings = PatientDoctorMapping.objects.filter(
            patient=patient
        ).select_related("patient", "doctor").order_by("-created_at")

        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Backward compatibility alias
PatientMappingView = MappingDetailView
