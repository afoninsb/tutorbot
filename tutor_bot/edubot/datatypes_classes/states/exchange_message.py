from django.conf import settings
from edubot.keyboards.inline import reply_kbrd
from edubot.main_classes import BotData, LocalData
from groups.models import Spisok


def message_to_admin(message: dict, bot: BotData, local: LocalData) -> None:
    """Сообщение ученика учителю.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Сообщение учителю'):
        cur_user = Spisok.objects.get(chat=local.chat_id)
        text = ('Сообщение от ученика: '
                f'{cur_user.first_name} {cur_user.last_name}\n\n')
        admins = local.admins
        for chat_id in admins.keys():
            answer = {
                'chat_id': chat_id,
                'text': text + message['text'],
                'reply_markup': reply_kbrd(local.chat_id),
            }
            bot.send_answer(answer)
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        local.user_edit(state='')
    elif message['text'] != 'Сообщение учителю':
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def message_to_admins(message: dict, bot: BotData, local: LocalData) -> None:
    """Сообщение Big_Boss`а всем админам.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Сообщение админам'):
        text = 'Сообщение от СуперБосса:\n'
        admins = local.all_admins_bots
        for chat_id in admins:
            answer = {
                'chat_id': chat_id,
                'text': f"{text}{message['text']}",
                'reply_markup': reply_kbrd(local.chat_id),
            }
            bot.send_answer(answer)
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        local.user_edit(state='')
    elif message['text'] != 'Сообщение админам':
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def support(message: dict, bot: BotData, local: LocalData) -> None:
    """Сообщение Big_Boss`а всем админам.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Техподдержка'):
        cur_user = Spisok.objects.get(chat=local.chat_id)
        text = ('Сообщение от админа: '
                f'{cur_user.first_name} {cur_user.last_name}\n'
                f'id: {cur_user.id}; chat-id: {cur_user.chat}\n\n')
        answer = {
            'chat_id': settings.BIG_BOSS_ID,
            'text': f"{text}{message['text']}",
            'reply_markup': reply_kbrd(local.chat_id),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        local.user_edit(state='')
    elif message['text'] != 'Техподдержка':
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def reply(message: dict, bot: BotData, local: LocalData) -> None:
    """Ответ на сообщение при переписке.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if bot.get_content_type(message) == 'text':
        chat_id = local.user_state.split(':')[1]
        text = f'Сообщение от: {local.user_full_name}\n\n'
        answer = {
            'chat_id': chat_id,
            'text': f"{text}{message['text']}",
            'reply_markup': reply_kbrd(local.chat_id),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        local.user_edit(state='')
    else:
        answer = {
            'chat_id': local.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)
