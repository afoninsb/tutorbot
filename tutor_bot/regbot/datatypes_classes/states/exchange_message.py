from django.conf import settings

from edubot.main_classes import BotData
from regbot.keyboards.inline import reply_kbrd


def message_to_admins(message: dict, bot: BotData, user) -> None:
    """Сообщение Big_Boss`а всем админам.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Сообщение админам'):
        text = 'Сообщение от СуперБосса:\n'
        admins = user.all_admins_bots
        for chat_id in admins:
            answer = {
                'chat_id': chat_id,
                'text': f"{text}{message['text']}",
                'reply_markup': reply_kbrd(user.chat_id),
            }
            bot.send_answer(answer)
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        user.edit(state='')
    elif message['text'] != 'Сообщение админам':
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def support(message: dict, bot: BotData, user) -> None:
    """Сообщение Big_Boss`а всем админам.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Техподдержка'):
        text = ('Сообщение от админа: '
                f'{user.full_name}\n'
                f'chatid: {user.chat_id}\n\n')
        answer = {
            'chat_id': settings.BIG_BOSS_ID,
            'text': f"{text}{message['text']}",
            'reply_markup': reply_kbrd(user.chat_id),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        user.edit(state='')
    elif message['text'] != 'Техподдержка':
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def reply(message: dict, bot: BotData, user) -> None:
    """Ответ на сообщение при переписке.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if bot.get_content_type(message) == 'text':
        cur_user = user.get_info
        chat_id = cur_user.state.split(':')[1]
        text = f'Сообщение от: {cur_user.first_name} {cur_user.last_name}\n\n'
        answer = {
            'chat_id': chat_id,
            'text': f"{text}{message['text']}",
            'reply_markup': reply_kbrd(user.chat_id),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        user.edit(state='')
    else:
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)
