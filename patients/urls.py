from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, DoctorViewSet

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")

urlpatterns = router.urls