from django.apps import AppConfig
from django.conf import settings


class RegbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'regbot'

    # def ready(self):
    #     from edubot.main_classes import BotData
    #     bot = BotData(settings.REGBOT_TOKEN)
    #     bot.commands = []
    #     if settings.DEBUG:
    #         data = {
    #             'url':
    #             f'https://c601-95-72-155-198.eu.ngrok.io/webhook/reg/{settings.REGBOT_TOKEN}/'
    #         }
    #     else:
    #         data = {
    #             'url':
    #             f'{settings.BASE_URL}/webhook/reg/{settings.REGBOT_TOKEN}/'
    #         }
    #     bot.set_webhook(data)
    #     bot.set_commands()
