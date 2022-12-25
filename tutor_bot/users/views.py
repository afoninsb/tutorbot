from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from bots.models import Bot
from bots.permissions import stop_bot
from users.models import AdminBot, Student, StudentBot


def index(request, botid):
    """Список учеников бота и заявок в бот."""
    cur_bot = get_object_or_404(Bot, id=botid)
    students = cur_bot.student_set.filter(studentbot__is_activated=True)
    students_new = cur_bot.student_set.filter(studentbot__is_activated=False)
    return render(request, 'users/index.html',
                  {'students': students, 'students_new': students_new})


def activate(request, botid):
    """Активация ученика в боте или удаление его заявки."""
    ids = request.POST.getlist('ids')
    if not ids:
        messages.error(request, 'Выберите учащегося!')
        return redirect('users:index', botid=botid)
    bulk_data = []
    for id in ids:
        if request.POST.get('activate_button'):
            cur_data = StudentBot.objects.get(
                bot__id=botid, student__id=id)
            cur_data.is_activated = True
            bulk_data.append(cur_data)
        else:
            Student.objects.filter(id=id).delete()

    if request.POST.get('activate_button'):
        StudentBot.objects.bulk_update(bulk_data, ('is_activated',))
        messages.success(request, 'Учащиеся активированы.')
        stop_bot(botid)
    else:
        messages.success(request, 'Учащиеся удалены.')
    return redirect('users:index', botid=botid)


def delete(request, botid, tgid):
    """Удаление ученика из бота."""
    try:
        get_object_or_404(AdminBot, tgid=tgid)
    except Exception:
        Student.objects.filter(tgid=tgid).delete()
        messages.success(request, 'Учащийся удалён.')
    else:
        messages.error(
            request, 'Вы не можете удалить себя из списка учащихся!')
    return redirect('users:index', botid=botid)
