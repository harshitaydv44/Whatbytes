from rest_framework import serializers

from .models import PatientDoctorMapping
from patients.models import Patient, Doctor


class PatientDoctorMappingSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        patient = data["patient"]
        doctor = data["doctor"]

        request = self.context.get("request")

        if request and patient.user_id != request.user.id:
            raise serializers.ValidationError(
                "You cannot assign a doctor to another user's patient."
            )

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor
        ).exists():
            raise serializers.ValidationError(
                "This doctor is already assigned to this patient."
            )

        return data