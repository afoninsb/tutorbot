from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render

from users.models import AdminBot


def index(request):
    """Тарифы ботов пользователя."""
    try:
        cur_admin = get_object_or_404(
            AdminBot, tgid=request.COOKIES.get('chatid'))
    except Exception:
        return HttpResponseForbidden()
    bots = cur_admin.bot.all().select_related('tarif')
    return render(request, 'tarifs/index.html', {'bots': bots, })
