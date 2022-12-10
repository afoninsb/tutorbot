from bots.models import Bot
from content.models import Category


def is_need_stop_bot(botid):
    if not Category.objects.\
            filter(bot__id=botid).filter(is_active=True).exists():
        Bot.objects.filter(id=botid).update(is_active=False)
