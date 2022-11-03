from bots.models import Bot
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from edubot.main_classes import BotData, LocalData
from groups.models import Group, Spisok
from kr.models import KROut
from plans.models import PlanItem
from works.models import Work


def push_work(
        message: dict, bot: BotData, local: LocalData
        ) -> None:
    """Сдача практической и контрольной работ.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    state = local.user_state.split(':')
    ok = False
    text = ('Я жду от вас <b>ссылку</b> на вашу работу'
            ' или <b>документ</b> с вашей работой:')
    content_type = bot.get_content_type(message)

    # Прислана ссылка
    if content_type == 'text':
        validate = URLValidator()
        try:
            validate(message['text'])
            link = message['text']
            ok = True
        except ValidationError:
            text = 'Присланная ссылка не рабочая! Пришлите другую:'

    # Прислан документ
    elif content_type == 'document':
        try:
            file_id = message['document']['file_id']
            file_url = bot.get_file({'file_id': file_id})
            file_name = message['document']['file_name']
            new_file_url = local.save_from_tg_to_works(
                file_url=file_url,
                file_name=file_name,
                type_dir=state[1],
                num_dir=state[2],
            )
            link = settings.MEDIA_URL + new_file_url
            ok = True
        except Exception:
            text = 'Не удалось получить и сохранить файл. Попробуйте ещё раз:'

    # Если всё хорошо, сохраняем информацию о присланной работе
    if ok:
        cur_bot = Bot.objects.get(tg=bot.token)
        cur_user = Spisok.objects.get(chat=local.chat_id)
        cur_item = PlanItem.objects.get(id=state[2])
        cur_group = Group.objects.get(id=state[3])
        new_work = Work.objects.create(
            user=cur_user,
            item=cur_item,
            bot=cur_bot,
            group=cur_group,
            type=state[1],
            link=link
        )
        if len(state) == 5:
            cur_kr_out = KROut.objects.get(id=state[4])
            Work.objects.filter(id=new_work.id).update(krout=cur_kr_out)
        text = 'Ваша работа принята!'
        local.user_edit(state='')
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)
