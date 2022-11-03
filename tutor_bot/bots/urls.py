from django.urls import path

from . import views

app_name = 'bots'

urlpatterns = [
    path('bot/<int:botid>/schedule/', views.botschedule, name='bot_schedule'),
    path('bot/<int:botid>/run/', views.botrunstop, name='bot_runstop'),
    path('bot/<int:botid>/del/', views.botdel, name='bot_del'),
    path('bot/<int:botid>/edit/', views.botedit, name='bot_edit'),
    path('bot/<int:botid>/pass/', views.botpass, name='bot_pass'),
    path('bot/<int:botid>/', views.bot, name='bot_page'),
    path('bot/add/', views.botadd, name='bot_add'),
    path('', views.index, name='index'),
]
