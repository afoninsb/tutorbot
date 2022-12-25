import os
import shutil
import uuid

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile


def handle_uploaded_file(file: InMemoryUploadedFile) -> str:
    """Сохраняем загружаемый файл во временную папку."""
    if not os.path.exists(settings.TEMP_ROOT):
        os.mkdir(settings.TEMP_ROOT, mode=0o777)
    new_name = uuid.uuid1()
    _, file_extension = os.path.splitext(file._name)
    file = f'{settings.TEMP_ROOT}/{new_name}{file_extension}'
    with open(file, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return f'{new_name}{file_extension}'


def replace_from_temp(**kwargs) -> str:
    """Перемещаем файл из временной папки в определяемую kwargs."""
    botid = kwargs.get('botid', False)
    img_name = kwargs.get('img_name', False)
    if not img_name:
        return None
    num_file = kwargs.get('num_file', False)
    num_dir = kwargs.get('num_dir', False)
    type_dir = kwargs.get('type_dir', False)
    name = img_name.replace(' ', '_')
    type_file = name.split('.')[-1]
    path_old = os.path.join(settings.TEMP_ROOT, name)
    name_new = f'{num_file}.{type_file}'
    path_new = os.path.join(
        settings.MEDIA_ROOT, str(botid), type_dir+str(num_dir), name_new)
    os.replace(path_old, path_new)
    return name_new


def del_file(**kwargs):
    """Удаляем файл."""
    if url := kwargs.get('url', False):
        path = str(url).split('/')
    path = os.path.join(settings.MEDIA_ROOT, *path)
    if os.path.isfile(path):
        os.remove(path)


def del_dir(**kwargs):
    """Удаляем каталог."""
    botid = kwargs.get('botid', False)
    path = os.path.join(settings.MEDIA_ROOT, str(botid))
    num_dir = kwargs.get('num_dir', False)
    type_dir = kwargs.get('type_dir', False)
    if num_dir and type_dir and type_dir != 'bot':
        path = os.path.join(path, type_dir+str(num_dir))
    if os.path.isdir(path):
        shutil.rmtree(path)


def add_dir(**kwargs):
    """Добавляем каталог."""
    botid = kwargs.get('botid', False)
    path = os.path.join(settings.MEDIA_ROOT, str(botid))
    num_dir = kwargs.get('num_dir', False)
    type_dir = kwargs.get('type_dir', False)
    if not num_dir and type_dir and type_dir != 'bot':
        path = os.path.join(path, type_dir)
    elif num_dir and type_dir and type_dir != 'bot':
        path = os.path.join(path, type_dir+str(num_dir))
    if not os.path.isdir(path):
        os.mkdir(path)
