""" Fortech URL Configuration """

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('_nested_admin/', include('nested_admin.urls')),

    # Аутентификация + Регистрация:
    path('api/v1/auth/', include('djoser.urls')),

    # Логин / Логаут: (auth/token/(login/logout))
    path('api/v1/auth/', include('djoser.urls.authtoken')),

    # Маршруты приложения
    path('api/v1/questionary/', include('testing_api.urls'))
]
