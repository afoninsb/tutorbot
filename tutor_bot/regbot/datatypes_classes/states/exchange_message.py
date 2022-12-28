from django.conf import settings
from typing import Any, Dict

from core.main_classes import BotData
from core.main_classes.localdata import UserData
from regbot.keyboards.inline import reply_kbrd


def message_to_admins(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Сообщение Big_Boss`а всем админам."""
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


def support(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Сообщение администратора в техподдержку."""
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Техподдержка'):
        text = ('Сообщение от админа: '
                f'{user.fullname}\n'
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


def reply(
        message: Dict[str, Any], bot: BotData, user: UserData
) -> None:
    """Ответ на сообщение при переписке."""
    if bot.get_content_type(message) == 'text':
        chat_id = user.state.split(':')[1]
        text = f'Сообщение от: {user.fullname}\n\n'
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
