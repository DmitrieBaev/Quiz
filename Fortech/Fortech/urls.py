""" Fortech URL Configuration """

from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация + Регистрация:
    path('api/v1/auth/', include('djoser.urls')),
    # Логин / Логаут: (auth/token/(login/logout))
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/v1/questionary/', include('testing_api.urls'))
    # path('api/v1/', include(router.urls)),
    # path('api/v1/questionary/', QuestionaryAPIView.as_view()),
    # path('api/v1/questionary/<int:questionary_id>/<int:pk>/', QuestionAPIView.as_view()),
]
