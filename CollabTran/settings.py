"""
Django settings for CollabTran project.

For more information on this file, see
https://docs.djangoproject.com/

"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from collections import OrderedDict

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^l)7d*%h&db4uft@dk%h-w&nup#pu%)a!d)c7jwgoixo5_hm0$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',
    # 'channels',
    'constance',
    'constance.backends.database',
    'WebApp',

]
INSTALLED_APPS += ("django_createsuperuserwithpassword",)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CollabTran.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'CollabTran.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {'default': dj_database_url.config(
    default='sqlite:////' + os.path.join(BASE_DIR, 'db.sqlite3'), conn_max_age=600)}

# if 'ThisIsHeroku' in os.environ:
#     # check if we are on Heroku
#     DATABASES = dj_database_url.config()
#
# else:
#     # this is for local deployment
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Django Channels
ASGI_APPLICATION = "CollabTran.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
        # Use a redis instance
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {"hosts": [("127.0.0.1", 6379)],},
    },
}
STATIC_ROOT = os.path.join(BASE_DIR, "WebApp/static")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = OrderedDict([
    ('SiteBase', ("https://ioe.edu.np", 'The base directory url to use.')),

    ('SITE_NAME', (0, '. . .')),
    ('Daily_Votes_Get', (5, 'Daily Votes User Get To Complete Quest')),
    ('Daily_Votes_Given', (5, 'Daily Votes User Give To Complete Quest')),
    ('Daily_Contributions', (5, 'Daily Contributions To Complete Quest')),

    ('Weekly_Votes_Get', (20, 'Weekly Votes User Get To Complete Quest')),
    ('Weekly_Votes_Given', (20, 'Weekly Votes User Give To Complete Quest')),
    ('Weekly_Contributions', (20, 'Weekly Contributions To Complete Quest')),

    ('Monthly_Votes_Get', (50, 'Monthly Votes User Get To Complete Quest')),
    ('Monthly_Votes_Given', (50, 'Monthly Votes User Give To Complete Quest')),
    ('Monthly_Contributions', (50, 'Monthly Contributions To Complete Quest')),

])

CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': ('SiteBase',),
    'Quest Options': {
        'fields': ('SITE_NAME', 'SITE_DESCRIPTION'),
        'collapse': False
    },
}

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/home'

LOGOUT_REDIRECT_URL = "/"
