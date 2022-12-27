from edubot.keyboards.inline import reply_kbrd
from edubot.main_classes import BotData
from edubot.main_classes.localdata import UserData


def message_to_admin(
        message: dict, bot: BotData, user: UserData, **kwargs
) -> None:
    """Сообщение ученика учителю.

    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if (bot.get_content_type(message) == 'text'
            and message['text'] != 'Сообщение учителю'):
        text = (f'Сообщение от ученика: {user.full_name}\n\n')
        teacher = user.teacher
        answer = {
            'chat_id': teacher.tgid,
            'text': text + message['text'],
            'reply_markup': reply_kbrd(user.chat_id),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        user.edit(state='')
    elif message['text'] != 'Сообщение учителю':
        answer = {
            'chat_id': user.chat_id,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)


def reply(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
    """Ответ на сообщение при переписке.

    Args:
        message (dict): объект message, полученный с вебхука.
    """
    if bot.get_content_type(message) == 'text':
        cur_user = user.get_info
        chat_id = cur_user.state.split(':')[1]
        text = f'Сообщение от: {cur_user.last_name} {cur_user.first_name}\n\n'
        answer = {
            'chat_id': chat_id,
            'text': f"{text}{message['text']}",
            'reply_markup': reply_kbrd(cur_user.tgid),
        }
        bot.send_answer(answer)
        answer = {
            'chat_id': cur_user.tgid,
            'text': 'Сообщение отправлено',
        }
        bot.send_answer(answer)
        user.edit(state='')
    else:
        answer = {
            'chat_id': cur_user.tgid,
            'text': 'Сообщение не отправлено. Можно отправлять ТОЛЬКО тексты!',
        }
        bot.send_answer(answer)
