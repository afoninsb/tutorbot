from django.urls import path

from . import views

app_name = 'tarifs'

urlpatterns = [
    path('', views.index, name='index'),
]
