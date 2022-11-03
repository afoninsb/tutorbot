from typing import Callable

from bots.models import Bot, BotAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from groups.models import Group
from kr.models import KR
from plans.models import Plan

# print(request.resolver_match.kwargs)  #

def is_yours(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        data = {'/plan/': Plan, '/group/': Group, '/kr/': KR}
        for small, big in data.items():
            if small in request.path and '/webhook/' not in request.path:
                txt = request.path.split('/')
                bot = txt[2]
                if txt[4].isdigit():
                    id = txt[4]
                    try:
                        big.objects.get(id=id, bot=bot)
                    except ObjectDoesNotExist:
                        mess = '<center><h2>Это не ваш контент!</h2></center>'
                        response = HttpResponse(mess)
                        return response
        response = get_response(request)
        return response

    return middleware


def is_admin(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        if (
            '/admin/' not in request.path
            and '/enter/' not in request.path
            and '/webhook/' not in request.path
            and '/works/' not in request.path
        ):
            if request.COOKIES.get('chatid'):
                try:
                    chat = request.COOKIES.get('chatid')
                    BotAdmin.objects.get(chat=chat)
                    response = get_response(request)
                except ObjectDoesNotExist:
                    mess = '<center><h2>Неизвестный пользователь</h2></center>'
                    response = HttpResponse(mess)
            else:
                mess = '<center><h2>Неизвестный пользователь</h2></center>'
                response = HttpResponse(mess)
        else:
            response = get_response(request)
        return response

    return middleware


def is_admin_bot(
    get_response: Callable[[HttpRequest], HttpResponse]
                ) -> Callable:

    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        if '/del/' not in request.path:
            chat = request.COOKIES.get('chatid')
            bots = Bot.objects.filter(admins__chat=chat)
            txt = request.path.split('/')
            if txt[1] == 'bot' and txt[2].isdigit():
                yes = False
                for bot in bots:
                    if bot.id == int(txt[2]):
                        yes = True
                        break
                if not yes:
                    mess = '<center><h2>Это не ваш бот!!!</h2></center>'
                    response = HttpResponse(mess)
        return response

    return middleware
