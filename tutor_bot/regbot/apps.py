from django.apps import AppConfig
from django.conf import settings


class RegbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regbot'

    def ready(self):
        from edubot.main_classes import BotData
        bot = BotData(settings.REGBOT_TOKEN)
        url = f'/webhook/reg/{settings.REGBOT_TOKEN}/'
        if settings.DEBUG:
            data = {
                'url': f'https://{settings.NGROK}{url}'
            }
        else:
            data = {
                'url': f'{settings.BASE_URL}{url}'
            }
        bot.set_webhook(data)
        bot.commands = [
            {
                'command': 'cancel',
                'description': 'Отменить текущую операцию'
            },
        ]
        bot.set_commands()
