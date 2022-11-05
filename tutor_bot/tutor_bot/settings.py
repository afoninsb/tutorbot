import os
from pathlib import Path

from dotenv import load_dotenv

DEBUG = True

load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))
BIG_BOSS_ID = os.getenv('BIG_BOSS_ID')
REGBOT_TOKEN = str(os.getenv('REGBOT_TOKEN'))

if DEBUG:
    BASE_URL = 'http://127.0.0.1:8000'
else:
    BASE_URL = 'http://studybot.fun'

BASE_DIR = Path(__file__).resolve().parent.parent

ALERT_MIN_TASKS = 10

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'ca46-95-72-155-198.eu.ngrok.io']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'bots',
    'content',
    'login',
    'edubot',
    'regbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middlewares.is_yours',
]

ROOT_URLCONF = 'tutor_bot.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'context_processors.conproc.get_admin',
                'context_processors.conproc.get_bot',
                'context_processors.conproc.alerts_newuser',
                'context_processors.conproc.alerts_endtask',
            ],
            'libraries': {
                'custom_tags': 'core.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'tutor_bot.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_URL = f'{MEDIA_URL}temp/'
TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')
