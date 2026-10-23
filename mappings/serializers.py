from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import UniqueTogetherValidator

from .models import PatientDoctorMapping
from patients.models import Patient, Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "created_at"]
        read_only_fields = ["id", "created_at"]
        validators = [
            UniqueTogetherValidator(
                queryset=PatientDoctorMapping.objects.all(),
                fields=["patient", "doctor"],
                message="This doctor is already assigned to this patient."
            )
        ]

    def validate(self, data):
        patient = data.get("patient")
        doctor = data.get("doctor")

        if self.instance:
            if patient is None:
                patient = self.instance.patient
            if doctor is None:
                doctor = self.instance.doctor

        request = self.context.get("request")

        # Enforce that user can only assign doctors to their own patients
        if request and patient and patient.user_id != request.user.id:
            raise PermissionDenied(
                "You cannot assign a doctor to another user's patient."
            )

        return data
