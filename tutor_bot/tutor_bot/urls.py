from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('bot/<int:botid>/tasks/', include('tasks.urls', namespace='tasks')),
    path('bot/<int:botid>/users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls', namespace='login')),
    path('', include('bots.urls', namespace='bots')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
