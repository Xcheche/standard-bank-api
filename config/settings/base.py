
# from pathlib import Path
# from dotenv import load_dotenv
# from os import getenv, path
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
from loguru import logger
from datetime import timedelta
import os
from loguru import logger
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR =BASE_DIR / "core_apps"
# local_env_file = path.join(BASE_DIR, ".env","env.local")

# if path.isfile(local_env_file):
#     load_dotenv(local_env_file)
# Load environment variables ONCE
load_dotenv(BASE_DIR / ".env" / "env.local")



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/



# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "drf_spectacular",
    "djoser",
    "cloudinary",
    "django_filters",
    "djcelery_email",
    "django_celery_beat",
]
LOCAL_APPS = [
    "core_apps.common.apps.CommonConfig",
    "core_apps.user_auth.apps.UserAuthConfig",
    "core_apps.user_profile.apps.UserProfileConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
AUTH_USER_MODEL = "user_auth.User"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST", "localhost"),
        "PORT": getenv("POSTGRES_PORT", "5432"),
    }
}

#================================================#
#Password Hashers#
#================================================#
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.SCryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



SITE_ID = 1





# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#========================================#
# Logging Configuration #
#========================================#


LOGGING_CONFIG = None  # Disable the default logging configuration

# Ensure the logs directory exists and is writable before loguru tries to
# open its file sinks. If we cannot create/write to the directory (e.g. the
# container user lacks permission), we fall back to a stderr-only sink so a
# logging misconfiguration can never prevent Django from booting.
LOGS_DIR = BASE_DIR / "logs"
_file_sinks_enabled = True
try:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    # Probe writability with a throwaway open() so a read-only bind mount
    # surfaces here rather than inside loguru's FileSink.
    probe_path = LOGS_DIR / ".loguru_write_probe"
    with open(probe_path, "a", encoding="utf-8"):
        pass
    probe_path.unlink(missing_ok=True)
except OSError:
    _file_sinks_enabled = False

_handlers = []

if _file_sinks_enabled:
    _handlers.extend(
        [
            {
                "sink": str(LOGS_DIR / "debug.log"),
                "level": "DEBUG",
                "filter": lambda record: record["level"].no <= logger.level("WARNING").no,
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                "{message}",
                "rotation": "10MB",
                "retention": "30 days",
                "compression": "zip",
            },
            {
                "sink": str(LOGS_DIR / "error.log"),
                "level": "ERROR",
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
                "{message}",
                "rotation": "10MB",
                "retention": "30 days",
                "compression": "zip",
                "backtrace": True,
                "diagnose": True,
            },
        ]
    )
else:
    # Last-resort fallback: log to stderr so we still get output when the
    # file sinks can't be created (e.g. PermissionError in the container).
    _handlers.append(
        {
            "sink": os.sys.stderr,
            "level": "DEBUG",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - "
            "{message}",
        }
    )

LOGURU_LOGGING = {"handlers": _handlers}

# Guard the configure call: a logging misconfiguration must never prevent
# Django from booting.
try:
    logger.configure(**LOGURU_LOGGING)
except Exception as _loguru_config_error:  # pragma: no cover - defensive
    import sys

    sys.stderr.write(f"[logging] loguru.configure() failed: {_loguru_config_error!r}\n")
    try:
        logger.remove()
        logger.add(os.sys.stderr, level="DEBUG")
    except Exception:
        pass

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"loguru": {"class": "interceptor.InterceptHandler"}},
    "root": {"handlers": ["loguru"], "level": "DEBUG"},
}