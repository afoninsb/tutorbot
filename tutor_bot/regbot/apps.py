from django.apps import AppConfig
from django.conf import settings


class RegbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regbot'


    def ready(self):
        from edubot.main_classes import BotData
        bot = BotData(settings.REGBOT_TOKEN)
        if settings.DEBUG:
            data = {
                'url': f'https://{settings.NGROK}/webhook/reg/{settings.REGBOT_TOKEN}/'
            }
        else:
            data = {
                'url': f'{settings.BASE_URL}/webhook/reg/{settings.REGBOT_TOKEN}/'
            }
        bot.set_webhook(data)
        bot.commands = [
            {
                'command': 'cancel',
                'description': 'Отменить текущую операцию'
            },
        ]
        bot.set_commands()
