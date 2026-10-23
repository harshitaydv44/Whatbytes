"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),

    path("api/auth/", include("accounts.urls")),
    path("api/", include("patients.urls")),
    path("api/mappings/", include("mappings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
