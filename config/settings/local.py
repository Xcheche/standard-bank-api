
from os import getenv
from .base import *  # noqa


# ========================================#
# Secret Key and Debug Configuration
# ========================================#

SECRET_KEY = getenv("SECRET_KEY", "unsafe-dev-key")

DEBUG = getenv("DEBUG", "False") == "True"


# ========================================#
# Hosts
# ========================================#

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


# ========================================#
# Admin URL Configuration
# ========================================#

ADMIN_URL = getenv("ADMIN_URL", "admin/")


SITE_NAME = getenv("SITE_NAME", "Standard Bank API")


# ========================================#
# Email Configuration
# ========================================#

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = getenv(
    "CELERY_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

EMAIL_HOST = getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = int(getenv("EMAIL_PORT", 25))
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL", "xcheche_bank <noreply@xcheche_bank.com>")


# ========================================#
# Domain Configuration
# ========================================#

DOMAIN = getenv("DOMAIN", "localhost:8000")


# ========================================#
# Image Configuration
# ========================================#

MAX_UPLOAD_SIZE = 1 * 1024 * 1024  # 1 MB


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    ]


# ========================================#
# Logout Duration after multiple failed login attempts
# ========================================#
LOGOUT_DURATION =timedelta(minutes=1)  # 1 hour in seconds


# ========================================#
# Login Attempts Configuration
# ========================================#
LOGIN_ATTEMPTS = 3
# ========================================#
# OTP Expiration Time Configuration
OTP_EXPIRATION_TIME = timedelta(minutes=1)  # 5 minutes in seconds


