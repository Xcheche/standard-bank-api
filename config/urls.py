# ===============================#
# Admin URL Configuration #
# ===============================#

from django.contrib import admin
from django.urls import path
from django.conf import settings
from core_apps.user_auth.views import TestLoggingView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# For the admin site branding, we need to import the admin module from config/admin.py
import config.admin  # noqa: F401  (registers our custom StandardBankAdminSite)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # Test Logging View
    path("", TestLoggingView.as_view(), name="test-logging"),
    #
    # API Documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]


# ===============================#
# Url Endpoints for Debugging and Development
# ===============================#
# Without nginx
"""
 - To access the admin site, use the following URL:
    http://localhost:8000/supersecret/
 - To access the API documentation, use the following URL:
    http://localhost:8000/api/v1/docs/
 - To access the ReDoc documentation, use the following URL:
    http://localhost:8000/api/v1/redoc/
"""
# With nginx
"""
- To access the admin site, use the following URL:
    http://0.0.0.0:8080/supersecret/
- To access the API documentation, use the following URL:
    http://0.0.0.0:8080/api/v1/docs/
- To access the ReDoc documentation, use the following URL:
    http://0.0.0.0:8080/api/v1/redoc/
"""
