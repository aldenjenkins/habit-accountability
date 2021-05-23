"""
Django settings for habits project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime
import os
import sys

from pathlib import Path

from habits.settings.utils import get_environ_setting, get_last_git_commit_hash
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://044c8a4f6fa04556954c9c69a5a22742@o192338.ingest.sentry.io/5778904",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

TESTING = (len(sys.argv) > 1 and sys.argv[1] == 'test') or bool(os.environ.get('FF_TESTING')) or 'pytest' in sys.modules
if TESTING:
    # compatibility with "pytest --numprocesses="
    # with pytest-xdist process, we have sys.argv = ['-c']
    os.environ['FF_TESTING'] = '1'

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
PROJECT_ROOT = here("..", "..")
root = lambda *x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Skip copying `node_modules/` files during `collectstatic` step.
# django-compressor will copy any required files from `node_modules/`.
STATICFILES_DIRS = (
   root('habits', 'static'),
)
if len(sys.argv) < 2 or not sys.argv[1] == 'collectstatic':
    STATICFILES_FINDERS += (
        'django.contrib.staticfiles.finders.FileSystemFinder',
    )

    STATICFILES_DIRS += (
        ('node_modules', root('node_modules')),
    )

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root('collected-static')


CURRENT_COMMIT_SHA = get_environ_setting('CURRENT_COMMIT_SHA', None) or get_last_git_commit_hash(
    PROJECT_ROOT
)
COMPRESS_OFFLINE_MANIFEST = 'manifest-{}.json'.format(CURRENT_COMMIT_SHA[:6])

# https://django-compressor.readthedocs.io/en/stable/settings/#django.conf.settings.COMPRESS_CSS_HASHING_METHOD
# Rely on ETag or Last-Modified HTTP response headers for cache busting instead
# of a query-string hash.
# Allows for preloading static files with `<link rel="preload">`.
COMPRESS_CSS_HASHING_METHOD = None

COMPRESS_BABEL_TRANSPILE = not TESTING

if not TESTING:

    # https://django-compressor.readthedocs.io/en/latest/settings/#django.conf.settings.COMPRESS_CACHEABLE_PRECOMPILERS
    COMPRESS_CACHEABLE_PRECOMPILERS = (
        'text/babel',
    )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("HABITS_SECRET", "abcdefg1234567890")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

REST_USE_JWT = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'webpack_loader',
    'compressor',
    'habits',
    'habits.mods.accountability',
    'habits.mods.calendar',
    'rest_auth'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=183),
}
ROOT_URLCONF = 'habits.urls'

CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3030',
] # If this is used, then not need to use `CORS_ORIGIN_ALLOW_ALL = True`
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3030',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'habits.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_environ_setting('DB_NAME', 'habits'),
        'USER': get_environ_setting('DB_USER', 'habits'),
        'PASSWORD': get_environ_setting('DB_PASSWORD', ''),
        'HOST': get_environ_setting('DB_HOST', '127.0.0.1'),
        'PORT': get_environ_setting('DB_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# app/webpack.py
from webpack_loader.loader import WebpackLoader

class CustomWebpackLoader(WebpackLoader):
    def filter_chunks(self, chunks):
        chunks = [chunk if isinstance(chunk, dict) else {'name': chunk} for chunk in chunks]
        return super().filter_chunks(chunks)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': root('webpack-stats.json'),
    }
}
