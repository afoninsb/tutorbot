import os
import sentry_sdk
from dotenv import load_dotenv
from pathlib import Path
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

DEBUG = os.getenv("DEBUG", 'False').lower() in ('true', '1', 't')

SECRET_KEY = str(os.getenv('SECRET_KEY'))

BIG_BOSS_ID = os.getenv('BIG_BOSS_ID')

BASE_DIR = Path(__file__).resolve().parent.parent

if DEBUG:
    REGBOT_TOKEN = str(os.getenv('TEMP_REGBOT_TOKEN'))

    NGROK = str(os.getenv('NGROK'))

    ALLOWED_HOSTS = ['127.0.0.1', NGROK]

    BASE_URL = 'http://127.0.0.1:8000'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    REGBOT_TOKEN = str(os.getenv('REGBOT_TOKEN'))

    ALLOWED_HOSTS = ['tutor.studybot.fun']

    BASE_URL = 'https://tutor.studybot.fun'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': str(os.getenv('BD_NAME')),
            'USER': str(os.getenv('BD_USER')),
            'PASSWORD': str(os.getenv('BD_PASSWORD')),
            'HOST': str(os.getenv('BD_HOST')),
            'PORT': '3306',
        }
    }
    
    sentry_sdk.init(
        dsn = str(os.getenv('SENTRY_DSN')),
        integrations = [DjangoIntegration()],
        traces_sample_rate = 1.0,
        send_default_pii = True
    )

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
    'stats',
    'tarifs',
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
                'core.conproc.get_context_data',
            ],
            'libraries': {
                'custom_tags': 'core.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'tutor_bot.wsgi.application'

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

else:

    STATIC_ROOT = os.path.join(BASE_DIR, "static") # Изначально пустой каталог, куда Django соберёт всё при выполнении manage.py collectstatic

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static_dev"), # Каталог, куда вам нужно складывать статику проекта, не относящуюся к конкретному приложению
    ]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_URL = f'{MEDIA_URL}temp/'

TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')

ALERT_MIN_TASKS = 10  # количество задач, ниже которого показывается оповещение

ALERT_END_TARIF = 3  # количество дней до окончания тарифа, ниже которого показывается оповещение

STUDENT_FREE_TARIF = 4  # количество учащихся в бесплатном тарифе = Количество учащихся + Сам админ-учитель (3+1=4 - 3 учащихся)
