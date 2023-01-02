import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Загрузка тестовой информации из csv-файла в базу данных.'''

    # имя файла с данными, приложение, модель
    DATA = (
        ('task.csv', 'content', 'Task'),
    )

    def handle(self, *args, **kwargs):
        message = 'Данные добавлены!'

        # Импорт данных из файлов в БД
        for fixture, app, model in self.DATA:

            # Импортрируем модель
            try:
                current_model = apps.get_model(app, model)
            except LookupError:
                message = (f'Данные не добавлены!!! '
                           f'Ошибка в наименованиях приложений и моделей: '
                           f'{app}, {model}')
                break

            # Получаем полный путь до файла с данными
            path_to_file = os.path.join(
                settings.BASE_DIR, 'content', 'management', 'commands', fixture
            )
            if not os.path.exists(path_to_file):
                message = (f'Данные не добавлены!!! '
                           f'Такой файл не существует: {path_to_file}')
                break

            with open(path_to_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                bot_id = 5529264374
                for row in reader:
                    title = row['text'][:50]
                    text = row['text']
                    answer = row['answer']
                    category_id = int(row['category_id']) + 14
                    task = current_model.objects.create(
                        title=title,
                        text=text,
                        answer=answer,
                        category_id=category_id,
                        bot_id=bot_id
                    )
                    if row['img']:
                        name = row['img'].split('/')[-1]
                        exp = name.split('.')[-1]
                        new_name = f'{task.id}.{exp}'
                        img = f'{bot_id}/cat{category_id}/{new_name}'
                        current_model.objects.filter(id=task.id).\
                            update(img=img)
                        path_old = os.path.join(
                            settings.BASE_DIR, 'content',
                            'management', 'commands', 'uploads', name
                        )
                        path_new = os.path.join(
                            settings.MEDIA_ROOT, str(bot_id),
                            f'cat{category_id}', new_name
                        )
                        os.replace(path_old, path_new)

        self.stdout.write(message)
