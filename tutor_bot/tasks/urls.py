from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('category/<int:categoryid>/task/<int:taskid>/del/', views.taskdel,
         name='task_del'),
    path('category/<int:categoryid>/task/<int:taskid>/edit/', views.taskedit,
         name='task_edit'),
    path('category/<int:categoryid>/task/<int:taskid>/', views.task,
         name='task'),
    path('category/<int:categoryid>/tasks/add/', views.taskadd,
         name='task_add'),
    path('category/<int:categoryid>/tasks/', views.categorytasks,
         name='category_tasks'),
    path('category/<int:categoryid>/del/', views.categorydel,
         name='category_del'),
    path('category/<int:categoryid>/edit/', views.categoryedit,
         name='category_edit'),
    path('category/<int:categoryid>/runstop/', views.categoryrunstop,
         name='category_runstop'),
    path('categories/add/', views.categoryadd, name='category_add'),
    path('categories/', views.category, name='category'),
]
