"""
Django settings for ardhi project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import environ
from django.contrib import staticfiles

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-w#w0w5wix&dswzd01j-(*uy(%%u^f8)ywl(c$4r%f!!+b=7nep'

# SECURITY WARNING: don't run with debug turned on in production!
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(env_file='.env')
SECRET_KEY = os.environ.get("SECRET_KEY")
# DEBUG = env('DEBUG')


# Application definition
DEBUG = True

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
# ALLOWED_HOSTS = []

# Application definition
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_HOST_USER = 'sambulikevin@gmail.com'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = env("EMAIL_BACKEND")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env("EMAIL_USE_TLS")
    EMAIL_PORT = env("EMAIL_PORT")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
]

THIRD_PIRTY_APPS = [
    'rest_framework',
    'rest_framework_gis',
    'leaflet',
    'djgeojson',
]

PROJECT_APPS = ['accounts', 'regions', 'parcels']

INSTALLED_APPS = DJANGO_APPS + THIRD_PIRTY_APPS + PROJECT_APPS

# user custom model setting
AUTH_USER_MODEL = 'accounts.Account'
# sign up form
SIGNUP_FORM_CLASS = 'accounts.forms.RegistrationForm'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    # 'accounts.backends.CaseInsensitiveModelBackend',
    )


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'ardhi.urls'

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


WSGI_APPLICATION = 'ardhi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': env("PG_ENGINE"),
#         'NAME': env("PG_NAME"),
#         'USER': env("PG_USER"),
#         'PASSWORD': env("PG_PASS"),
#         'HOST': env("PG_DB_HOST"),
#         'PORT': env("PG_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'Ardhi',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PASSWORD': 'kevoh',
        'PORT': '5432'
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, '/static'),)

# leaflet configuration
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-1.22488, 36.827164),
    'DEFAULT_ZOOM': 16,
    'MAX_ZOOM': 20,
    'MIN_ZOOM': 5,
    'SCALE': 'both',
    'MINIMAP': True,
    'ATTRIBUTION_PREFIX': 'Map by Kevin Sambuli Amuhaya',
    'TILES':
        [('Satellite', 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
          {'maxZoom': 19,
           'attribution': '&copy; <a ''href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}),

         ('Topography', 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
          {'maxZoom': 17,
           'attribution': 'Map data: &copy; <a' 'href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
                          'contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a '
                          'href="https://opentopomap.org">OpenTopoMap</a> (<a '
                          'href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'}),

         ('Stamen Toner', 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}{r}.{ext}', {
             'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
                            '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data '
                            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
             'subdomains': 'abcd', 'minZoom': 0, 'maxZoom': 20, 'ext': 'png'
         }),

         ('Terrain', 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}', {
             'maxZoom': 20,
             'attribution': 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
         }),
         ]
}

# geoip configuration
GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')
GEOIP_CITY = os.path.join(BASE_DIR, 'geoip/GeoLite2-City')
GEOIP_COUNTRY = os.path.join(BASE_DIR, 'geoip/GeoLite2-Country')

#  serialization class
SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson",
}

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#     ]
# }

# django redis cache

# CACHE_TTL = 60 * 1500
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# celery url

# CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# CELERY_RESULT_BACKEND = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")
# BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Africa/Nairobi'

# using django redis for sessions
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.TokenAuthentication',
#     )
# }

# STREAM_API_KEY = YOUR_STREAM_API_KEY # https://getstream.io/dashboard/
# STREAM_API_SECRET = YOUR_STREAM_API_SECRET
# DJOSER = {
#     'SERIALIZERS': {
#         'token': 'auth.serializers.StreamTokenSerializer',
#     }
# }



# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# redis_host = os.environ.get('REDIS_HOST', 'localhost')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
