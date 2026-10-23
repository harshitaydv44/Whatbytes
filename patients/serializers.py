from rest_framework import serializers
from .models import Patient, Doctor


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Patient name cannot be blank.")
        return stripped

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError(
                "Age must be between 0 and 120."
            )
        return value


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone",
            "email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):
        stripped = value.strip()
        if not stripped:
            raise serializers.ValidationError("Doctor name cannot be blank.")
        return stripped

    def validate_email(self, value):
        return value.strip().lower()
