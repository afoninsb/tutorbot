# """Класс для работы с базой данных."""

# import os
# from uuid import uuid1

# import requests
# from bots.models import Bot, BotAdmin
# from django.conf import settings
# from django.shortcuts import get_object_or_404
# from groups.models import Spisok
# from regbot.models import Temp
# from works.models import Work

# from .dataclass import DataClass


# class LocalData(DataClass):

#     def __init__(
#             self,
#             token: str,
#             chat_id: int,
#             **kwargs,
#     ):
#         self.token = token
#         self.chat_id = chat_id

#     @property
#     def user_is_in_base(self) -> bool:
#         """Есть ли юзер в базе данных?
#         Returns:
#             bool: Истина, если есть,
#                   Ложь, если нет.
#         """
#         try:
#             get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return False
#         return True

#     @property
#     def user_new(self) -> None:
#         """Помещаем в базу нового юзера и связываем с ботом."""
#         Spisok.objects.create(
#             chat=self.chat_id,
#             first_name='fn',
#             last_name='ln',
#             state='start'
#         )

#     @property
#     def user_is_in_bot(self) -> bool:
#         """Есть ли юзер в боте?
#         Returns:
#             bool: Истина, если есть,
#                   Ложь, если нет.
#         """
#         try:
#             cur_bot = get_object_or_404(Bot, tg=self.token)
#             cur_user = get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return False
#         return cur_user in cur_bot.spisok.all()

#     @property
#     def user_to_bot(self) -> None:
#         """Связываем юзера и бота."""
#         try:
#             cur_bot = get_object_or_404(Bot, tg=self.token)
#             cur_user = get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return 0
#         cur_user.bots.add(cur_bot)

#     @property
#     def user_state(self) -> str:
#         """Получаем состояние юзера.
#         Returns:
#             str: состояние юзера.
#         """
#         try:
#             user = get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return ''
#         return user.state

#     @property
#     def user_first_name(self) -> str:
#         """Получаем имя юзера.
#         Returns:
#             str: Имя юзера.
#         """
#         try:
#             user = get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return ''
#         return user.first_name

#     @property
#     def user_full_name(self) -> str:
#         """Получаем полное имя юзера.
#         Returns:
#             str: Имя Фамилия юзера.
#         """
#         try:
#             user = get_object_or_404(Spisok, chat=self.chat_id)
#         except Exception:
#             return ''
#         return f'{user.first_name} {user.last_name}'

#     def user_edit(self, **kwargs) -> None:
#         """Меняем Имя, Фамилию, Состояние юзера."""
#         Spisok.objects.filter(chat=self.chat_id).update(**kwargs)

#     @property
#     def temp_admin_new(self) -> bool:
#         """Открываем запись о потенциальном админе.
#         Returns:
#             bool: Истина, если админ новый,
#                   Ложь, если этот chat_id уже админ.
#         """
#         try:
#             get_object_or_404(BotAdmin, chat=self.chat_id)
#         except Exception:
#             Temp.objects.get_or_create(
#                 chat=self.chat_id,
#                 first_name='fn',
#                 last_name='ln',
#                 org='org',
#                 position='pos',
#                 why='why'
#             )
#             return True
#         return False

#     def temp_admin_edit(self, **kwargs) -> None:
#         """Меняем информацию о потенциальном админе."""
#         Temp.objects.filter(chat=self.chat_id).update(**kwargs)

#     @property
#     def admins(self) -> dict:
#         """Получение словаря админов бота.
#         Returns:
#             dict: Словарь админов {chat_id: 'Fn Ln'}.
#         """
#         try:
#             cur_bot = get_object_or_404(Bot, tg=self.token)
#         except Exception:
#             return {}
#         admins_all = cur_bot.admins.all()
#         return {admin.chat: f"{admin.first_name} {admin.last_name}"
#                 for admin in admins_all}

#     @property
#     def all_admins_bots(self) -> list:
#         """Получение списка всех админов ботов.
#         Returns:
#             dict: Список админов (chat_id).
#         """
#         admins_all = BotAdmin.objects.all()
#         return (admin.chat for admin in admins_all)

#     @property
#     def bot_password(self) -> str:
#         """Получение пароля бота.
#         Returns:
#             str: пароль бота.
#         """
#         try:
#             cur_bot = get_object_or_404(Bot, tg=self.token)
#         except Exception:
#             return ''
#         return cur_bot.password

#     def save_from_tg_to_works(
#             self,
#             file_url: str,
#             file_name: str,
#             type_dir: str,
#             num_dir: int) -> str:
#         """
#         Сохранение на локальный диск файла,
#         присланного пользователем в бот.
#         Args:
#             file_url (str): url-адрес присланного файла.
#             file_name (str): имя присланного файла.
#             type_dir (str): тип директории для сохранения файла.
#             num_dir (int): номер директории для сохранения файла.
#         Returns:
#             str: url-адрес сохранённого файла.
#         """
#         botid = self.token.split(':')[0]
#         num_dir = str(num_dir)
#         path = os.path.join(settings.MEDIA_ROOT, str(botid), 'works')
#         path = os.path.join(path, type_dir + num_dir)
#         if not os.path.isdir(path):
#             os.mkdir(path)
#         add_name = str(uuid1())
#         file_ext = file_name.split('.')[-1]
#         file_name = f'{self.chat_id}-{add_name}.{file_ext}'
#         file_path = os.path.join(path, file_name)
#         with open(file_path, "wb") as f:
#             try:
#                 ufr = requests.get(file_url)
#             except Exception:
#                 return ''
#             f.write(ufr.content)
#         return f'{botid}/works/{type_dir}{num_dir}/{file_name}'

#     def get_status_work(self, item, group_id):
#         cur_user = Spisok.objects.get(chat=self.chat_id)
#         work = Work.objects.filter(
#             user=cur_user,
#             item=item,
#             group__id=group_id).first()
#         if work:
#             if work.status == 'passed':
#                 return 'Сдано'
#             if work.status == 'done':
#                 return 'Зачет'
#             if work.status == 'rejected':
#                 return 'Не зачет'
#         return 'Сдать'
