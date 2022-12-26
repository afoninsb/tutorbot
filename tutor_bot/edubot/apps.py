from django.apps import AppConfig
from django.conf import settings


class EdubotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edubot'

    def ready(self):
        from bots.models import Bot

        from .main_classes import BotData

        if bots := Bot.objects.all():
            for bot in bots:
                bot = BotData(bot.token)
                url = f'/webhook/{bot.token}/'
                if settings.DEBUG:
                    data = {
                        'url': f'https://{settings.NGROK}{url}'
                    }
                else:
                    data = {
                        'url': f'{settings.BASE_URL}{url}'
                    }
                bot.set_webhook(data)
                bot.set_commands()
