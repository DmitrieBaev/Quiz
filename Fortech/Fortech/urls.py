""" Fortech URL Configuration """

from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from testing_api.views import *

# router = routers.SimpleRouter()
# router.register(r'questionary', QuestionaryViewSet, basename='questionary')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('api/v1/', include(router.urls)),
    # path('api/v1/questionary/', QuestionaryAPIView.as_view()),
    # path('api/v1/questionary/<int:questionary_id>/<int:pk>/', QuestionAPIView.as_view()),
]
