from django.conf import settings
from django.conf.urls.static import static
# По умолчанию в проект Django подключена система администрирования
from django.contrib import admin
# Функция include позволит использовать path() из других файлов.
from django.urls import include, path

urlpatterns = [
    # Дорогой Джанго, если на сервер пришёл любой запрос (''),
    # перейди в файл urls приложения posts
    # и проверь там все path() на совпадение с запрошенным URL
    path('', include('posts.urls', namespace='posts')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace='users')),
    # Все адреса с префиксом auth/ если (не найдуться ранее)
    # будут перенаправлены в модуль django.contrib.auth
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
