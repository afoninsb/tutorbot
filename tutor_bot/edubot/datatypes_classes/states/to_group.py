from groups.models import Group, Spisok
from edubot.main_classes import BotData, LocalData


def user_to_group(message: dict, bot: BotData, local: LocalData) -> None:
    """Вступление юзера в группу.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    text = 'Такой группы нет. Вводите пин-код внимательнее:'
    if message.get('text'):
        cur_group = Group.objects.filter(pin=message.get('text'))
        if cur_group:
            cur_user = Spisok.objects.filter(chat=local.chat_id)
            cur_group[0].users.add(cur_user[0])
            local.user_edit(state='')
            text = f'Вы добавлены в группу {cur_group[0].name}'
    answer = {
        'chat_id': local.chat_id,
        'text': text,
    }
    bot.send_answer(answer)
