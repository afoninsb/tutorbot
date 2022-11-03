from typing import Callable

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse

from bots.models import Bot
from tasks.models import Category, Task
from users.models import AdminBot


def is_yours(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        if (request.path in ('/', '/bots/add/')
                or '/admin/' in request.path
                or '/login/' in request.path
                or '/webhook/' in request.path):
            response = get_response(request)
            return response
        tgid = request.COOKIES.get('chatid')
        name_model = {
            'bot': Bot,
            'category': Category,
            'task': Task,
        }
        get_ids = request.path.split('/')
        name_id = {}
        for name in name_model:
            if name in get_ids:
                name_id[name] = get_ids[get_ids.index(name) + 1]
        botid = name_id['bot']
        for name, id in name_id.items():
            try:
                if name == 'bot':
                    Bot.objects.get(id=botid, admin__tgid=tgid)
                else:
                    name_model[name].objects.get(id=id, bot__id=botid)
            except ObjectDoesNotExist:
                mess = '<center><h2>У вас нет доступа к этому контенту</h2></center>'
                response = HttpResponse(mess)
            else:
                response = get_response(request)
        return response

    return middleware


def is_admin(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        if not (
            '/admin/' in request.path
            or '/login/' in request.path
            or '/webhook/' in request.path
        ):
            if request.COOKIES.get('chatid'):
                try:
                    AdminBot.objects.get(tgid=request.COOKIES.get('chatid'))
                except ObjectDoesNotExist:
                    mess = '<center><h2>Неизвестный пользователь</h2></center>'
                    response = HttpResponse(mess)
                else:
                    response = get_response(request)
            else:
                mess = '<center><h2>Неизвестный пользователь</h2></center>'
                response = HttpResponse(mess)
        else:
            response = get_response(request)
        return response

    return middleware
