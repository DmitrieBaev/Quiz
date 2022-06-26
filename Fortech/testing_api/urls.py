""" Маршруты в приложении """

from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuestionaryAPIView.as_view(), name='questionary'),
    path('<int:questionary_id>/', views.QuestionAPIView.as_view(), name='question'),
    path('user-answer/', views.UserAnswerCreateAPIView.as_view(), name='user-answer'),
    path('<int:questionary_id>/result', views.ResultsAPIView.as_view(), name='user-answer-result'),
]
