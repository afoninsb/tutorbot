"""Класс для работы с информацией, полученной с вебхука."""

import json

import requests

from .dataclass import DataClass


class BotData(DataClass):

    def __init__(
            self,
            token: str,
            **kwargs,
    ):
        self.token = token
        self.url = f'https://api.telegram.org/bot{self.token}/'
        self.commands = [
            {
                'command': 'change_name',
                'description': 'Изменить Имя и/или Фамилию'
            },
            {
                'command': 'cancel',
                'description': 'Отменить текущую операцию'
            },
        ]

    def user_id(self, data: dict) -> int:
        """Получение chat id пользователя в Telegram.
        Args:
            data (dict): обновление, поступившее на вебхук.
        Returns:
            int: chat id пользователя в Telegram.
        """
        message_object = self.get_message(data)
        if 'chat' in message_object:
            return message_object['chat'].get('id', 0)
        if 'from' in message_object:
            return message_object['from'].get('id', 0)
        return 0

    @property
    def bot_id(self):
        return self.token.split(':')[0]

    @staticmethod
    def get_message(data: dict) -> dict:
        """Получение объекта message.
        Args:
            data (dict): обновление, поступившее на вебхук.
        Returns:
            dict: объект message.
        """
        if 'message' in data:
            return data['message']
        if 'callback_query' in data:
            return data['callback_query'].get('message', {})
        return {}

    def send_answer(self, answer: dict) -> None:
        """Отправка сообщения в бот.
        Args:
            data (dict): параметры команды sendMessage.
        """
        method = f'{self.url}sendMessage'
        try:
            requests.post(method, data=answer)
        except Exception:
            return 0

    def send_photo(self, data: dict) -> None:
        """Отправка изображения в бот.
        Args:
            data (dict): параметры команды sendPhoto.
        """
        method = f'{self.url}sendPhoto'
        try:
            requests.post(method, data=data)
        except Exception:
            return 0

    def delete_webhook(self) -> None:
        """Удаление вебхука бота."""
        method = f'{self.url}deleteWebhook'
        try:
            requests.post(method)
        except Exception:
            return 0

    def set_webhook(self, data: dict) -> None:
        """Установка веб-хука бота.
        Args:
            data (dict): параметры метода setWebhook.
        """
        method = f'{self.url}setWebhook'
        try:
            requests.post(method, data=data)
        except Exception:
            return 0

    def set_commands(self) -> None:
        """Установка комманд бота."""
        method = f'{self.url}setMyCommands'
        commands = str(json.dumps(self.commands))
        send_text = f'{method}?commands={commands}'
        try:
            requests.get(send_text)
        except Exception:
            return 0

    @staticmethod
    def get_content_type(message: dict) -> str:
        """Получение типа контента, поступвшего на вебхук.
        Args:
            message (dict): message из поступившего вебхука.
        Returns:
            str: контент обновления.
        """
        contents = ['text', 'document', 'photo']
        return next(
            (content for content in contents if content in message), '')

    @staticmethod
    def get_data_type(data: dict) -> str:
        """Получение типа обновления, поступвшего на вебхук.
        Args:
            data (dict): обновление, поступившее на вебхук.
        Returns:
            str: тип обновления.
        """
        if 'callback_query' in data:
            return 'callback_query'
        if 'message' in data:
            if 'text' in data['message']:
                if data['message']['text'].startswith('/'):
                    return 'command'
                else:
                    return 'text'
        return ''
