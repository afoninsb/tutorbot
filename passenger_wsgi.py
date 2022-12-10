# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/a/afoninry/tutor.studybot.fun/tutor_bot')
sys.path.insert(1, '/home/a/afoninry/tutor.studybot.fun/venv_django/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'tutor_bot.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()