from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuestionaryAPIView.as_view(), name='questionary'),
    path('<int:questionary_id>/', views.QuestionAPIView.as_view(), name='question'),
    path('user-answer/', views.UserAnswerCreateAPIView.as_view(), name='user-answer'),

    # path('api/v1/', include(router.urls)),
    # path('api/v1/questionary/', QuestionaryAPIView.as_view()),
    # path('api/v1/questionary/<int:questionary_id>/<int:pk>/', QuestionAPIView.as_view()),
]
