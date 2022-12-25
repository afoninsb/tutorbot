from django.urls import path

from . import views

app_name = 'stats'

urlpatterns = [
    path('user/<int:user_id>/<int:cat_id>/<str:pin>/',
         views.usercatstat, name='usercatstat'),
    path('user/<int:user_id>/<str:pin>/', views.userstat, name='userstat'),
    path('task/<int:task_id>/', views.task, name='task'),
    path('cat/<int:cat_id>/<str:user_id>/', views.category, name='category'),
    path('allcat/<str:user_id>/', views.all_categories, name='all_categories'),
    path('rating/', views.rating, name='rating'),
]
