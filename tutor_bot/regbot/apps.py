from django.apps import AppConfig
from django.conf import settings


class RegbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regbot'

    def ready(self):
        from edubot.main_classes import BotData
        bot = BotData(settings.REGBOT_TOKEN)
        data = {
            'url': f'https://9fd4-95-73-109-218.eu.ngrok.io/webhook/reg/{settings.REGBOT_TOKEN}/'
            # 'url': f'{settings.BASE_URL}/webhook/reg/{settings.REGBOT_TOKEN}/'
        }
        bot.set_webhook(data)
        bot.commands = [
            {
                'command': 'cancel',
                'description': 'Отменить текущую операцию'
            },
        ]
        bot.set_commands()
