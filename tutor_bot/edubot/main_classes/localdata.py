"""Класс для работы с базой данных."""

import hashlib
from datetime import datetime
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from bots.models import Bot
from content.models import Log, Task
from regbot.models import Temp
from stats.models import Rating
from users.models import AdminBot, Student, StudentBot

from .dataclass import DataClass


class UserData(DataClass):

    def __init__(
            self,
            chat_id: int,
            model,
            **kwargs,
    ):
        self.chat_id = chat_id
        self.model = model

    @property
    def is_in_base(self) -> bool:
        """Есть ли юзер в базе данных?
        Returns:
            bool: Истина, если есть,
                  Ложь, если нет.
        """
        try:
            get_object_or_404(self.model, tgid=self.chat_id)
        except Exception:
            return False
        return True

    def to_base(self, **kwargs) -> bool:
        """Открываем запись юзера в базе.
        Returns:
            bool: Истина, если админ новый,
                  Ложь, если этот chat_id уже админ.
        """
        try:
            get_object_or_404(self.model, tgid=self.chat_id)
        except Exception:
            self.model.objects.create(**kwargs)
            return True
        return False

    @property
    def get_info(self):
        try:
            return get_object_or_404(self.model, tgid=self.chat_id)
        except Exception:
            return False

    @property
    def full_name(self):
        if cur_user := self.get_info:
            return f'{cur_user.last_name} {cur_user.first_name}'

    def edit(self, **kwargs) -> None:
        """Меняем информацию о юзере."""
        self.model.objects.filter(tgid=self.chat_id).update(**kwargs)


class AdminUser(UserData):
    def __init__(
            self,
            chat_id: int,
            **kwargs,
    ):
        super().__init__(chat_id, model=AdminBot)

    @property
    def admin_bots(self) -> set:
        """Получение списка токенов ботов админа.
        Returns:
            set: Список ботов (tokens).
        """
        bots = Bot.objects.filter(admin__tgid=self.chat_id)
        return (bot.token for bot in bots)

    @property
    def all_admins_bots(self) -> tuple:
        """Получение списка всех админов всех ботов.
        Returns:
            list: Список админов (chat_id).
        """
        admins_all = AdminBot.objects.all()
        return (admin.tgid for admin in admins_all)


class TempUser(UserData):
    def __init__(
            self,
            chat_id: int,
            **kwargs,
    ):
        super().__init__(chat_id, model=Temp)

    def is_right_bot_password(self, bot, password) -> bool:
        """Сравнение введённого пародя с паролем бота.
        Returns:
            bool: равны?
        """
        password = hashlib.pbkdf2_hmac(
            'sha256',
            str(password).encode('utf-8'),
            b'',
            100000,
            dklen=128
        )
        try:
            cur_bot = get_object_or_404(Bot, token=bot.token)
        except Exception:
            return False
        return str(password) == str(cur_bot.password)

    def delete(self, **kwargs) -> None:
        """Удаляем временного юзера."""
        self.model.objects.filter(tgid=self.chat_id).delete()


class StudentUser(UserData):
    def __init__(
            self,
            chat_id: int,
            token: str,
            **kwargs,
    ):
        super().__init__(chat_id, model=Student)
        self.token = token
        self.edit(pin='')

    @property
    def user_id(self):
        try:
            cur_user = get_object_or_404(
                Student,
                tgid=self.chat_id,
                bot__token=self.token,
            )
        except Exception:
            return None
        return cur_user.id

    @property
    def is_in_bot(self) -> bool:
        """Студент в этом боте?.
        Returns:
            bool: в боте?
        """
        try:
            get_object_or_404(
                Student,
                tgid=self.chat_id,
                bot__token=self.token,
            )
        except Exception:
            return False
        return True

    @property
    def teacher(self) -> QuerySet:
        """tgid учителя.
        Returns:
            queryset: учитель
        """
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
        except Exception:
            return 0
        return cur_bot.admin

    @property
    def to_bot(self):
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
        except Exception:
            return 0
        try:
            cur_student = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return 0
        try:
            StudentBot.objects.create(
                bot=cur_bot,
                student=cur_student,
            )
        except Exception:
            return 0

    @property
    def get_rating(self):
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
        except Exception:
            return
        try:
            rating_data = Rating.objects.filter(bot=cur_bot).\
                filter(time=datetime.now().strftime('%Y-%m-%d')).\
                select_related('student')
        except Exception:
            return
        if not rating_data:
            return
        tgids = []
        rating = []
        for number, rtng in enumerate(rating_data):
            tgids.append(rtng.student.tgid)
            rating.append((rtng.student.tgid, number+1, rtng.score))
        number = tgids.index(self.chat_id)
        user_rating = []
        if number > 1:
            user_rating.append(rating[number-2])
        if number > 0:
            user_rating.append(rating[number-1])
        user_rating.append(rating[number])
        if number < len(tgids)-1:
            user_rating.append(rating[number+1])
        if number < len(tgids)-2:
            user_rating.append(rating[number+2])
        return user_rating


class TaskData(DataClass):

    def __init__(
            self,
            task_id: int,
            **kwargs,
    ):
        self.task_id = task_id

    @property
    def get_all_info(self):
        """Получаем всю инфу о задании.
        Returns:
            queryset: инфо о задании
        """
        task = Task.objects.filter(
            id=self.task_id).select_related('category', 'bot')
        return task[0]

    @staticmethod
    def save_log(**kwargs):
        """Сохраняем лог о выполнении задания."""
        cur_student = get_object_or_404(Student, tgid=kwargs['student'].chat_id)
        Log.objects.create(
            student=cur_student,
            task=kwargs['task'],
            category=kwargs['category'],
            answer=kwargs['answer'],
            is_truth=kwargs['is_truth'],
            bot=kwargs['bot']
        )

    def count_logs(self, user: StudentUser) -> int:
        """Получаем количество ответов на вопрос в логе.
        Args:
            student: StudentUser - объект модели Студента.
        Returns:
            int: количество ответов студента на текущий вопрос.
        """
        return Log.objects.filter(
            student__tgid=user.chat_id, task__id=self.task_id
        ).count()

    @property
    def get_param(self) -> dict:
        """Получаем параметры ответа в боте.
        Returns:
            dict: словарь двух парамтеров.
        """
        cur_bot = self.get_all_info.bot
        return {
            'is_show_wrong_right': cur_bot.is_show_wrong_right,
            'is_show_answer': cur_bot.is_show_answer,
        }
