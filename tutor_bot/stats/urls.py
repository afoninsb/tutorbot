from django.urls import path

from . import views

app_name = 'stats'

urlpatterns = [
    path('task/<int:task_id>/', views.task, name='task'),
    path('cat/<int:cat_id>/<str:user_id>/', views.category, name='category'),
    path('allcat/<str:user_id>/', views.all_categories, name='all_categories'),
]
