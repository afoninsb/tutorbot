from typing import Callable

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from bots.models import Bot
from content.models import Category, Task
from users.models import AdminBot


def is_yours(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        if (request.path in ('/', '/bots/add/')
                or '/favicon.ico' in request.path
                or '/admin/' in request.path
                or '/del/' in request.path
                or '/login/' in request.path
                or '/media/' in request.path
                or '/webhook/' in request.path):
            return get_response(request)

        tgid = request.COOKIES.get('chatid')
        try:
            AdminBot.objects.get(tgid=tgid)
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
        else:
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
            botid = name_id.get('bot')
            try:
                for name, obj_id in name_id.items():
                    if name == 'bot':
                        Bot.objects.get(id=botid, admin__tgid=tgid)
                    else:
                        name_model[name].objects.get(id=obj_id, bot__id=botid)
            except ObjectDoesNotExist:
                return HttpResponseForbidden()
            else:
                response = get_response(request)
            return response

    return middleware
