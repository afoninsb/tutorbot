import os
import shutil
from faker import Faker
from django.conf import settings


def handle_uploaded_file(f):
    if not os.path.exists(settings.TEMP_ROOT):
        os.mkdir(settings.TEMP_ROOT, mode=0o777)
    fake = Faker()
    new_name = ''.join(fake.words(nb=5))
    _, file_extension = os.path.splitext(f._name)
    file = f'{settings.TEMP_ROOT}/{new_name}{file_extension}'
    with open(file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f'{new_name}{file_extension}'


def replace_from_temp(**kwargs):
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
    if url := kwargs.get('url', False):
        path = str(url).split('/')
    path = os.path.join(settings.MEDIA_ROOT, *path)
    if os.path.isfile(path):
        os.remove(path)


def del_dir(**kwargs):
    botid = kwargs.get('botid', False)
    path = os.path.join(settings.MEDIA_ROOT, str(botid))
    num_dir = kwargs.get('num_dir', False)
    type_dir = kwargs.get('type_dir', False)
    if num_dir and type_dir and type_dir != 'bot':
        path = os.path.join(path, type_dir+str(num_dir))
    if os.path.isdir(path):
        shutil.rmtree(path)


def add_dir(**kwargs):
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
