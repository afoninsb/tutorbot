from edubot.main_classes import BotData
from edubot.main_classes.localdata import StudentUser, TaskData, UserData


def answer(message: dict, bot: BotData, user: UserData, **kwargs) -> None:
    """Сдача работ.
    Args:
        message (dict): объект message, полученный с вебхука.
    """
    task_id = user.get_info.state.split(':')[1]
    text = f'Я жду от вас <b>текстовый ответ</b> на задание {task_id}'
    if bot.get_content_type(message) == 'text':
        user.edit(state='')
        if kwargs['is_admin']:
            student_user = StudentUser(user.chat_id, bot.token)
        else:
            student_user = user
        task = TaskData(task_id)
        cur_task = task.get_all_info
        is_truth = str(message['text']) == str(cur_task.answer)
        diff = cur_task.difficulty
        score = cur_task.difficulty if is_truth else 0
        task.save_log(
            student=student_user,
            task=cur_task,
            category=cur_task.category,
            answer=message['text'],
            is_truth=is_truth,
            score=score,
            bot=cur_task.bot
        )
        text = 'Ваш ответ принят!'
        param = task.get_param
        if param['is_show_wrong_right']:
            text = f'{text}\nВаш ответ '
            text = f'{text}правильный.' if is_truth else f'{text}неправильный.'
        if param['is_show_answer'] and not is_truth:
            text = f'{text}\nПравильный ответ: {cur_task.answer}'
    answer = {
        'chat_id': user.chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    bot.send_answer(answer)
