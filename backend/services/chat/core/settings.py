"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("TESTING")

ALLOWED_HOSTS = ["*"]

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.environ.get("ELASTICSEARCH_PORT")

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "websocket",
    "scripts",
    "search",
    "rest_framework"
]

ASGI_APPLICATION = "core.asgi.application"


if DEBUG:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer",
        }
    }
    LOGFILE_NAME = "test.log"

else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(REDIS_HOST, REDIS_PORT)],
            },
        }
    }
    LOGFILE_NAME = os.environ.get("LOGFILE_NAME")

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]


ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        # "ENGINE": "django.db.backends.sqlite3",
        "ENGINE": 'django_prometheus.db.backends.sqlite3',
        "NAME": BASE_DIR / "db.sqlite3",
        "TEST": {"NAME": BASE_DIR / "test_db.sqlite3"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_MANAGEMENT_URL = os.environ.get("AUTH_MANAGEMENT_URL")

LOGGING = {
    "version": 1,
    # The version number of our log
    "disable_existing_loggers": False,
    # django uses some of its own loggers for internal operations. In case you want to disable them just replace the False above with true.
    # A handler for WARNING. It is basically writing the WARNING messages into a file called WARNING.log
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / LOGFILE_NAME,
        },
    },
    # A logger for WARNING which has a handler called 'file'. A logger can have multiple handler
    "loggers": {
        # notice the blank '', Usually you would put built in loggers like django or root here based on your needs
        "": {
            # notice how file variable is called in handler which has been defined above
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": True,
        },
    },
}
