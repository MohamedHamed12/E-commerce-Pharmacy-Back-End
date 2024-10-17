# -*- coding: utf-8 -*-
"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the django-insecure-5^31#!z1k!=(+*w7g+&qjw#in1sb7!(2bc7bsf(7kciy0_35@ysecret key used in production secret!
SECRET_KEY = config("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # added apps
    "accounts",
    "products",
    "pharmacy",
    "orders",
    "chat",
    "ai",
    # rest framework
    "rest_framework",
    "rest_framework.authtoken",
    # allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    # dj-rest-auth
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # cors headers
    "corsheaders",
    # filters
    "django_filters",
]

MIDDLEWARE = [
    # cors headers
    "corsheaders.middleware.CorsMiddleware",
    # default
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # allauth
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "project.urls"

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

WSGI_APPLICATION = "project.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    # 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


###### REST FRAMEWORK ######

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        # "accounts.custom_jwt.CustomJWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
}


###### ALLAUTH ######
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_PASSWORD_MIN_LENGTH = 8

###### SITE ######
SITE_ID = 1
SITE_NAME = "Backend"


##### EMAIL ######
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

##### AUTHENTICATION_BACKENDS  ######
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

####### REST_AUTH #######

REST_AUTH = {"USE_JWT": True, "JWT_AUTH_HTTPONLY": False}

####### swagger #######
INSTALLED_APPS += [
    "drf_yasg",
]

####### static files #######

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static")


###### database #######

###### Media #######
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


##### cors headers  #######

CORS_ALLOW_HEADERS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

SWAGGER_URLS = None
SWAGGER_SETTINGS = {
    "SECURITY_SCHEMES": {
        "Bearer": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
}


#
CSRF_TRUSTED_ORIGINS = [
    "https://ikseer.azurewebsites.net",
    "https://ikseer.onrender.com",
    "https://ikseer2.azurewebsites.net",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),  # Short expiration for security
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # Adjust based on requirements
}

AUTH_USER_MODEL = "accounts.CustomUser"


### CACHING ###
# settings.py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "django_cache"),
    }
}


DROPBOX_APP_KEY = config("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = config("DROPBOX_APP_SECRET")

INSTALLED_APPS += ("storages",)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.dropbox.DropboxStorage",
        "OPTIONS": {},
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DROPBOX_OAUTH2_REFRESH_TOKEN = config("DROPBOX_OAUTH2_REFRESH_TOKEN")


# REGISTER_SERIALIZER="accounts.serializers.RegistrationSerializerSettings"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}


# Time after which OTP will expire
EXPIRY_TIME = 120  # seconds

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": config("gclient_id", ""),  # replace me
            "secret": config("gsecret", ""),  # replace me
            "key": "",  # leave empty
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "VERIFIED_EMAIL": True,
    },
}


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("gclient_id", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("gclient_id", "")
