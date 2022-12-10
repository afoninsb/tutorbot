from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from users.models import AdminBot


def enter(request, chatid, pin):
    if request.COOKIES.get('chatid'):
        response = HttpResponse("Cookie deleted")
        response.delete_cookie("chatid")
    try:
        AdminBot.objects.get(tgid=chatid, pin=pin)
        AdminBot.objects.filter(tgid=chatid).update(pin='')
        response = HttpResponseRedirect(reverse('bots:index'))
        response.set_cookie(
            key='chatid',
            value=chatid,
            secure=True,
            max_age=36000)
    except ObjectDoesNotExist:
        mess = '<center><h2>Неизвестный пользователь</h2></center>'
        response = HttpResponse(mess)
    return response


def logout(request):
    response = HttpResponse('<center><h2>До свидания!</h2></center>')
    response.delete_cookie("chatid")
    return response
