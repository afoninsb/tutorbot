from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('bot/<int:botid>/stats/',
         include('stats.urls', namespace='stats')),
    path('bot/<int:botid>/content/',
         include('content.urls', namespace='content')),
    path('bot/<int:botid>/users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls', namespace='login')),
    path('webhook/reg/', include('regbot.urls', namespace='regbot')),
    path('webhook/', include('edubot.urls', namespace='edubot')),
    path('', include('bots.urls', namespace='bots')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
