from django.urls import path

from . import views

app_name = 'login'

urlpatterns = [
    path('enter/<int:chatid>/<slug:pin>/', views.enter, name='enter'),
    path('logout/', views.logout, name='logout'),
]