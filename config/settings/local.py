from os import getenv, path # noqa
from pathlib import Path # noqa
from dotenv import load_dotenv # noqa

from .base import * # noqa
from .base import BASE_DIR  # noqa

local_env_file = path.join(BASE_DIR, ".env", "env.local")

# "django-insecure-jdt%41^unr(pwg#5+$vk5zk2yats3-8b^aetl%2k!$&-p7#z1s"


if path.isfile(local_env_file):
    load_dotenv(local_env_file)

#========================================#
# Secret Key and Debug Configuration #
#========================================#
SECRET_KEY = getenv("SECRET_KEY")
DEBUG = getenv("DEBUG")
SITE_NAME = getenv("SITE_NAME")
ALLOWED_HOSTS = ["localhost","127.0.0.1","0.0.0.0"]

#========================================#
# Admin URL Configuration #
#========================================#
ADMIN_URL = getenv("ADMIN_URL")

#========================================#
# Email Configuration #
#========================================#
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
CELERY_EMAIL_BACKEND = getenv("EMAIL_BACKEND")
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
DEFAULT_FROM_EMAIL = getenv("DEFAULT_FROM_EMAIL")

#========================================#
# Domain Configuration #
#========================================#
DOMAIN = getenv("DOMAIN")

#========================================#
# Image Configuration #
#========================================#
MAX_UPLOAD_SIZE = 1 * 1024 * 1024  # 1 MB



