from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('delete/<int:tgid>/', views.delete, name='delete'),
    path('activate/', views.activate, name='activate'),
    path('', views.index, name='index'),
]
