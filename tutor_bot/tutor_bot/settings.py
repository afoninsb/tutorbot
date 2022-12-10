import os
from dotenv import load_dotenv
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


DEBUG = False

load_dotenv()

SECRET_KEY = str(os.getenv('SECRET_KEY'))
BIG_BOSS_ID = os.getenv('BIG_BOSS_ID')
REGBOT_TOKEN = str(os.getenv('REGBOT_TOKEN'))

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['tutor.studybot.fun', 'www.tutor.studybot.fun']
BASE_URL = 'https://tutor.studybot.fun'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': str(os.getenv('BD_NAME')),
        'USER': str(os.getenv('BD_USER')),
        'PASSWORD': str(os.getenv('BD_PASSWORD')),
        'HOST': str(os.getenv('BD_HOST')),
    }
}

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

sentry_sdk.init(
    dsn="https://348c2e42e3174c7d8fd195de012cba9a@o4504303315582976.ingest.sentry.io/4504303320301568",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static") # Изначально пустой каталог, куда Django соберёт всё при выполнении manage.py collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_dev"), # Каталог, куда вам нужно складывать статику проекта, не относящуюся к конкретному приложению
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_URL = f'{MEDIA_URL}temp/'
TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')

ALERT_MIN_TASKS = 10
