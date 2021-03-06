"""
Django settings for socialabstraction project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import typing

from urllib.parse import ParseResult, urlparse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '71y4t#j*-qrjtc7f2u_r(z(vnyh(6vg4*b8f_+x(ck@yk(3r85'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ['DEBUG'] in ['f', 'false', 'no'] else True

ALLOWED_HOSTS = ['psf.jbcurtin.io']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'socialloginapp',
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

ROOT_URLCONF = 'socialabstraction.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'socialabstraction.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

PSQL_URL: str = os.environ['PSQL_URL']
_parts: ParseResult = urlparse(PSQL_URL)
identity, host_conn = _parts.netloc.split('@')
username, password = identity.split(':')
host, port = host_conn.split(':')
database: str = _parts.path.strip('/')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': database,
        'USER': username,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Custom settings
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
AUTHENTICATION_BACKENDS = [
  'social_core.backends.open_id.OpenIdAuth',
  'social_core.backends.facebook.FacebookOAuth2',
  'social_core.backends.google.GoogleOpenId',
  'social_core.backends.google.GoogleOAuth2',
  'social_core.backends.google.GoogleOAuth',
  'social_core.backends.twitter.TwitterOAuth',
  'social_core.backends.yahoo.YahooOpenId',
  'django.contrib.auth.backends.ModelBackend',
]
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range, picture{url}',
}
SOCIAL_AUTH_FACEBOOK_API_VERSION = '3.2'
SOCIAL_AUTH_PIPELINE = (
  'social_core.pipeline.social_auth.social_details',
  'social_core.pipeline.social_auth.social_uid',
  'social_core.pipeline.social_auth.auth_allowed',
  'social_core.pipeline.social_auth.social_user',
  'social_core.pipeline.user.get_username',
  'social_core.pipeline.user.create_user',
  'social_core.pipeline.social_auth.associate_user',
  'social_core.pipeline.social_auth.load_extra_data',
  'social_core.pipeline.user.user_details',
  'socialloginapp.pipeline.user_picture',
  'socialloginapp.pipeline.user_login',
)
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = 'https://psf.jbcurtin.io/index.html'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_HEADERS: typing.Dict[str, str] = {
  'Accept': 'application/json',
  'User-Agent': 'https://github.com/jbcurtin/socialabstraction'
}
AUTH_USER_MODEL = 'socialloginapp.SocialLoginAppUser'
MEDIA_ROOT: str = 'uploaded-files'
MEDIA_URL: str = '/media/'
STATIC_URL: str = '/static/'
STATIC_ROOT: str = 'static-files'
