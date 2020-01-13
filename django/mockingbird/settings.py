"""
Django settings for mockingbird project.
Generated by 'django-admin startproject' using Django 2.2.3.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DJANGO_ENV = os.environ.get("DJANGO_ENV", "local")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j!8l9$b(2=ngj&=4%+ds4$si1p8nq&%760+w3i43w@8148)040'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =True

ALLOWED_HOSTS = ['teammockingbird333.herokuapp.com', '127.0.0.1', 'localhost']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Application definition

INSTALLED_APPS = [
    'widget_tweaks',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # borrowed
   'multiselectfield',
   'phone_field',


    # created
    'chat',
    'onboard',
    'match',
    'tags',
    'account',
    'survey',
    'feedback',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'mockingbird.urls'

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

ASGI_APPLICATION = "mockingbird.routing.application"
WSGI_APPLICATION = 'mockingbird.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {}
if DJANGO_ENV == "local":
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mockingbird_db_local',
        'USER': 'mockingbird_admin',
        'PASSWORD': 'mockingbird_password_local',
        'HOST': 'localhost',
        'PORT': '54320',
    }
elif DJANGO_ENV == "production":
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)
else:
    raise Exception(f"Not a valid DJANGO_ENV: {DJANGO_ENV}")

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

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Celery stuff
# CELERY_BROKER_URL=os.environ.get('REDIS_URL', '')
# CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', '')
BROKER_URL = 'redis://h:ped0612c2ab8f1af2281848fbdce999d9e4c5f420ebf81c6c028a1cc85602b55a@ec2-54-88-173-114.compute-1.amazonaws.com:13639'
CELERY_RESULT_BACKEND = 'redis://h:ped0612c2ab8f1af2281848fbdce999d9e4c5f420ebf81c6c028a1cc85602b55a@ec2-54-88-173-114.compute-1.amazonaws.com:13639'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TIMEZONE = TIME_ZONE

# redis_host = os.environ.get('REDIS_HOST', 'ec2-54-164-134-74.compute-1.amazonaws.com')
# redis_host = os.environ.get('REDIS_HOST', 'redis://localhost:6379')
redis_host = os.environ.get('REDIS_HOST', 'ec2-54-88-173-114.compute-1.amazonaws.com')
# redis_host = os.environ.get(BROKER_URL)
# Channel layer definitions
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation asgi_redis
        # "BACKEND": "asgi_redis.RedisChannelLayer",
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [BROKER_URL],
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

STATIC_ROOT = PROJECT_DIR  # os.path.join(PROJECT_DIR, 'static')
STATICFILE_DIRS = PROJECT_DIR
STATICFILE_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages"
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# will need to change for production
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'MockingBird <noreply@mockingbird.com>'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'teammockingbird333@gmail.com'
EMAIL_HOST_PASSWORD = 'mockingbirdteam333'
