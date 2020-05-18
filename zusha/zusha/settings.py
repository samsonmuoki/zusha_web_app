"""
Django settings for zusha project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from celery.schedules import crontab


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hm=f0aql1tc!s2$aenq+991t5lds-d@3o9t$i%!4+(a=kr*dp1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'zusha.duckdns.org',
    'localhost'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'registration.apps.RegistrationConfig',
    'registrations.apps.RegistrationsConfig',
    'reports.apps.ReportsConfig',
    'django_celery_results',
    'django_celery_beat',
    'qr_code',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zusha.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zusha.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zusha',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

QR_CODE_CACHE_ALIAS = 'qr-code'

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

# celery setting.
CELERY_CACHE_BACKEND = 'default'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
    # 'qr-code': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'qr-code-cache',
    #     'TIMEOUT': 3600
    # }
}


BROKER_HOST = os.getenv("BROKER_HOST", "zusha")
BROKER_PORT = os.getenv("BROKER_PORT", "5672")
BROKER_USER = os.getenv("BROKER_USER", "zusha")
BROKER_PASSWORD = os.getenv("BROKER_PASSWORD", "zusha")
BROKER_VHOST = os.getenv("BROKER_VHOST", "zushavhost")
CELERY_RESULT_BACKEND = "rpc://"
CELERY_RESULT_PERSISTENT = False
CELERY_TASK_RESULT_EXPIRES = 300
CELERY_TIMEZONE = "Africa/Nairobi"
CELERY_DEFAULT_QUEUE = os.getenv("CELERY_QUEUE", "zusha")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"


CELERY_BEAT_SCHEDULE = {
    # 'reports.tasks.send_alerts': {
    #     'task': 'tasks.send_alerts',
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'schedule': crontab(),  # execute every minute
    #     # 'args': (16, 16),
    # },
    'send-alerts': {
        # 'task': 'zusha.reports.tasks.blacklist_vehicles',
        'task': 'reports.tasks.send_alerts',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(),  # execute every minute
    },
    'zusha.reports.tasks.blacklist_vehicles': {
        # 'task': 'zusha.reports.tasks.blacklist_vehicles',
        'task': 'reports.tasks.blacklist_vehicles',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(),  # execute every minute
    },
    'zusha.reports.tasks.blacklist_saccos': {
        # 'task': 'zusha.reports.tasks.blacklist_saccos',
        'task': 'reports.tasks.blacklist_saccos',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(),  # execute every minute
    },
    'zusha.reports.tasks.blacklist_drivers': {
        # 'task': 'zusha.reports.tasks.blacklist_drivers',
        'task': 'reports.tasks.blacklist_drivers',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'schedule': crontab(),  # execute every minute
    },
}

if DEBUG:
    CELERY_TASK_ALWAYS_EAGER = True


# FIREBASE CONFIGURATIONS
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "")
FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN", "")
FIREBASE_DATABASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET", "")
FIREBASE_MESSAGING_SENDER_ID = os.getenv("FIREBASE_MESSAGING_SENDER_ID", "")
FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID", "")
FIREBASE_MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID", "")
FIREBASE_USER = os.getenv("FIREBASE_USER", "")
FIREBASE_PASSWORD = os.getenv("FIREBASE_PASSWORD", "")
