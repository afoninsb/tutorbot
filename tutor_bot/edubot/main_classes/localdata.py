"""Класс для работы с базой данных."""

from django.shortcuts import get_object_or_404

from bots.models import Bot
from regbot.models import Temp
from users.models import AdminBot, Student
from .dataclass import DataClass


class LocalData(DataClass):

    def __init__(
            self,
            token: str,
            chat_id: int,
            **kwargs,
    ):
        self.token = token
        self.chat_id = chat_id

    @property
    def user_is_in_base(self) -> bool:
        """Есть ли юзер в базе данных?
        Returns:
            bool: Истина, если есть,
                  Ложь, если нет.
        """
        try:
            get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return False
        return True

    @property
    def user_new(self) -> None:
        """Помещаем в базу нового юзера и связываем с ботом."""
        Student.objects.create(
            tgid=self.chat_id,
            first_name='fn',
            last_name='ln',
            state='start'
        )

    @property
    def user_is_in_bot(self) -> bool:
        """Есть ли юзер в боте?
        Returns:
            bool: Истина, если есть,
                  Ложь, если нет.
        """
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
            cur_user = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return False
        return cur_user in cur_bot.student.all()

    @property
    def user_to_bot(self) -> None:
        """Связываем юзера и бота."""
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
            cur_user = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return 0
        cur_user.bot.add(cur_bot)

    @property
    def user_state(self) -> str:
        """Получаем состояние юзера.
        Returns:
            str: состояние юзера.
        """
        try:
            cur_user = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return ''
        return cur_user.state

    @property
    def user_first_name(self) -> str:
        """Получаем имя юзера.
        Returns:
            str: Имя юзера.
        """
        try:
            cur_user = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return ''
        return cur_user.first_name

    @property
    def user_full_name(self) -> str:
        """Получаем полное имя юзера.
        Returns:
            str: Имя Фамилия юзера.
        """
        try:
            cur_user = get_object_or_404(Student, tgid=self.chat_id)
        except Exception:
            return ''
        return f'{cur_user.first_name} {cur_user.last_name}'

    def user_edit(self, **kwargs) -> None:
        """Меняем Имя, Фамилию, Состояние юзера."""
        Student.objects.filter(tgid=self.chat_id).update(**kwargs)

    @property
    def temp_admin_new(self) -> bool:
        """Открываем запись о потенциальном админе.
        Returns:
            bool: Истина, если админ новый,
                  Ложь, если этот chat_id уже админ.
        """
        try:
            get_object_or_404(AdminBot, tgid=self.chat_id)
        except Exception:
            Temp.objects.get_or_create(
                tgid=self.chat_id,
                first_name='fn',
                last_name='ln',
                org='org',
                position='pos',
                why='why',
                state='start',
            )
            return False
        return True

    def temp_admin_edit(self, **kwargs) -> None:
        """Меняем информацию о потенциальном админе."""
        Temp.objects.filter(tgid=self.chat_id).update(**kwargs)

    @property
    def temp_admin_state(self) -> str:
        """Получаем состояние потенциального админа.
        Returns:
            str: состояние потенциального админа.
        """
        try:
            cur_user = get_object_or_404(Temp, tgid=self.chat_id)
        except Exception:
            return ''
        return cur_user.state

    @property
    def admin_state(self) -> str:
        """Получаем состояние потенциального админа.
        Returns:
            str: состояние потенциального админа.
        """
        try:
            cur_user = get_object_or_404(AdminBot, tgid=self.chat_id)
        except Exception:
            return ''
        return cur_user.state

    @property
    def admins(self) -> dict:
        """Получение словаря админов бота.
        Returns:
            dict: Словарь админов {chat_id: 'Fn Ln'}.
        """
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
        except Exception:
            return {}
        admins_all = cur_bot.admin.all()
        return {admin.chat: f"{admin.first_name} {admin.last_name}"
                for admin in admins_all}

    @property
    def all_admins_bots(self) -> list:
        """Получение списка всех админов всех ботов.
        Returns:
            dict: Список админов (chat_id).
        """
        admins_all = AdminBot.objects.all()
        return (admin.tgid for admin in admins_all)

    @property
    def bot_password(self) -> str:
        """Получение пароля бота.
        Returns:
            str: шифрованный пароль бота.
        """
        try:
            cur_bot = get_object_or_404(Bot, token=self.token)
        except Exception:
            return ''
        return cur_bot.password
