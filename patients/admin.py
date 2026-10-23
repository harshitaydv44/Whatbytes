from django.contrib import admin
from .models import Patient, Doctor


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age", "gender", "user")
    search_fields = ("name", "phone")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "specialization", "email")
    search_fields = ("name", "specialization", "email")