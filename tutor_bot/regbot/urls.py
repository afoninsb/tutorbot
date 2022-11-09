from django.urls import path

from . import views

app_name = 'regbot'

urlpatterns = [
    path('<str:bot_tg>/', views.webhook, name='webhook'),
]
