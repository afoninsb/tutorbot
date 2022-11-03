from django.urls import path

from . import views

app_name = 'edubot'

urlpatterns = [
    path('<str:bot_tg>/', views.webhook, name='webhook'),
]
