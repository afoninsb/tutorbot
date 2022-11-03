from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from bots.models import Bot
from users.models import Student


def index(request, botid):
    cur_bot = get_object_or_404(Bot, id=botid)
    students = cur_bot.student.filter(is_activated=True)
    students_new = cur_bot.student.filter(is_activated=False)
    return render(request, 'users/index.html',
                  {'students': students, 'students_new': students_new})


def activate(request, botid):
    tgids = request.POST.getlist('tgids')
    if not tgids:
        messages.error(request, 'Выберите учащегося!')
        return redirect('users:index', botid=botid)
    for tgid in tgids:
        if request.POST.get('activate_button'):
            Student.objects.filter(tgid=tgid).update(is_activated=True)
            messages.success(request, 'Учащиеся активированы.')
        else:
            Student.objects.filter(tgid=tgid).delete()
            messages.success(request, 'Учащиеся удалены.')
    return redirect('users:index', botid=botid)


def delete(request, botid, tgid):
    Student.objects.filter(tgid=tgid).delete()
    messages.success(request, 'Учащийся удалён.')
    return redirect('users:index', botid=botid)
