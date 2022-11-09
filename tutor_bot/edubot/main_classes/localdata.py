"""Класс для работы с базой данных."""

from django.shortcuts import get_object_or_404
import hashlib

from bots.models import Bot
from regbot.models import Temp
from users.models import AdminBot, Student
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
    def all_admins_bots(self) -> list:
        """Получение списка всех админов всех ботов.
        Returns:
            dict: Список админов (chat_id).
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

    def delete(self, **kwargs) -> None:
        """Меняем информацию о юзере."""
        self.model.objects.filter(tgid=self.chat_id).delete()





class LocalData(DataClass):

    def __init__(
            self,
            chat_id: int,
            **kwargs,
    ):
        self.chat_id = chat_id
        
    # @property
    # def user_is_in_base(self) -> bool:
    #     """Есть ли юзер в базе данных?
    #     Returns:
    #         bool: Истина, если есть,
    #               Ложь, если нет.
    #     """
    #     try:
    #         get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return False
    #     return True

    # @property
    # def user_new(self) -> None:
    #     """Помещаем в базу нового юзера и связываем с ботом."""
    #     Student.objects.create(
    #         tgid=self.chat_id,
    #         first_name='fn',
    #         last_name='ln',
    #         state='start'
    #     )

    # @property
    # def user_is_in_bot(self) -> bool:
    #     """Есть ли юзер в боте?
    #     Returns:
    #         bool: Истина, если есть,
    #               Ложь, если нет.
    #     """
    #     try:
    #         cur_bot = get_object_or_404(Bot, token=self.token)
    #         cur_user = get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return False
    #     return cur_user in cur_bot.student.all()

    # @property
    # def user_to_bot(self) -> None:
    #     """Связываем юзера и бота."""
    #     try:
    #         cur_bot = get_object_or_404(Bot, token=self.token)
    #         cur_user = get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return 0
    #     cur_bot.student.add(cur_user)

    # @property
    # def user_state(self) -> str:
    #     """Получаем состояние юзера.
    #     Returns:
    #         str: состояние юзера.
    #     """
    #     try:
    #         cur_user = get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return ''
    #     return cur_user.state

    # @property
    # def user_first_name(self) -> str:
    #     """Получаем имя юзера.
    #     Returns:
    #         str: Имя юзера.
    #     """
    #     try:
    #         cur_user = get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return ''
    #     return cur_user.first_name

    # @property
    # def user_full_name(self) -> str:
    #     """Получаем полное имя юзера.
    #     Returns:
    #         str: Имя Фамилия юзера.
    #     """
    #     try:
    #         cur_user = get_object_or_404(Student, tgid=self.chat_id)
    #     except Exception:
    #         return ''
    #     return f'{cur_user.first_name} {cur_user.last_name}'

    # def user_edit(self, **kwargs) -> None:
    #     """Меняем Имя, Фамилию, Состояние юзера."""
    #     Student.objects.filter(tgid=self.chat_id).update(**kwargs)

    # @property
    # def is_admin(self) -> bool:
    #     """Юзер админ?.
    #     Returns:
    #         bool: Истина, если админ ,
    #               Ложь, если нет.
    #     """
    #     try:
    #         get_object_or_404(AdminBot, tgid=self.chat_id)
    #     except Exception:
    #         return False
    #     return True

    # def admin_edit(self, **kwargs) -> None:
    #     """Меняем информацию о потенциальном админе."""
    #     AdminBot.objects.filter(tgid=self.chat_id).update(**kwargs)

    # @property
    # def temp_admin_create(self) -> bool:
    #     """Открываем запись о потенциальном админе.
    #     Returns:
    #         bool: Истина, если админ новый,
    #               Ложь, если этот chat_id уже админ.
    #     """
    #     try:
    #         get_object_or_404(Temp, tgid=self.chat_id)
    #     except Exception:
    #         Temp.objects.get_or_create(
    #             tgid=self.chat_id,
    #             first_name='fn',
    #             last_name='ln',
    #             org='org',
    #             position='pos',
    #             why='why',
    #             state='start',
    #         )
    #         return True
    #     return False

    # def temp_admin_edit(self, **kwargs) -> None:
    #     """Меняем информацию о потенциальном админе."""
    #     Temp.objects.filter(tgid=self.chat_id).update(**kwargs)

    # @property
    # def temp_admin_state(self) -> str:
    #     """Получаем состояние потенциального админа.
    #     Returns:
    #         str: состояние потенциального админа.
    #     """
    #     try:
    #         cur_user = get_object_or_404(Temp, tgid=self.chat_id)
    #     except Exception:
    #         return ''
    #     return cur_user.state

    # @property
    # def admin_state(self) -> str:
    #     """Получаем состояние админа.
    #     Returns:
    #         str: состояние потенциального админа.
    #     """
    #     try:
    #         cur_user = get_object_or_404(AdminBot, tgid=self.chat_id)
    #     except Exception:
    #         return False
    #     return cur_user.state

    # @property
    # def admins(self) -> dict:
    #     """Получение словаря админов бота.
    #     Returns:
    #         dict: Словарь админов {chat_id: 'Fn Ln'}.
    #     """
    #     try:
    #         cur_bot = get_object_or_404(Bot, token=self.token)
    #     except Exception:
    #         return {}
    #     admins_all = cur_bot.admin.all()
    #     return {admin.chat: f"{admin.first_name} {admin.last_name}"
    #             for admin in admins_all}

    # @property
    # def all_admins_bots(self) -> list:
    #     """Получение списка всех админов всех ботов.
    #     Returns:
    #         dict: Список админов (chat_id).
    #     """
    #     admins_all = AdminBot.objects.all()
    #     return (admin.tgid for admin in admins_all)

    # def is_right_bot_password(self, password) -> bool:
    #     """Сравнение введённого пародя с паролем бота.
    #     Returns:
    #         bool: равны?
    #     """
    #     try:
    #         cur_bot = get_object_or_404(Bot, token=self.token)
    #     except Exception:
    #         return False
    #     password = hashlib.md5(password.encode())
    #     return password == cur_bot.password
