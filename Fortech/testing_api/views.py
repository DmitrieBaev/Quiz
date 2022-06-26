""" Представления """

from rest_framework import generics, views, response, authentication, permissions, viewsets

from .models import Question, Questionary, UserAnswer, Answer
from .paginations import QuestionAPIPagination
from .serializers import QuestionarySerializer, QuestionSerializer, UserAnswerSerializer_Setter, UserAnswerSerializer_Getter


class QuestionaryAPIView(generics.ListAPIView):
    """ Отображение списка вопросников """

    queryset = Questionary.objects.all()
    serializer_class = QuestionarySerializer


class QuestionAPIView(views.APIView):
    """ Получение вопросов из выбранного вопросника """

    pagination_class = QuestionAPIPagination
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        """
        Переопределение получения значений

        :param kwargs: Забираем идентификатор Вопросника
        """

        question = Question.objects.filter(questionary__pk=kwargs['questionary_id'])
        page = self.paginate_queryset(question)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = QuestionSerializer(question, many=True)
        return response.Response(serializer.data)

    @property
    def paginator(self):
        """ Экземпляр пагинатора, связанный с представлением, или `None`. """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """ Возвращает одну страницу результатов или `None`, если нумерация страниц отключена. """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """ Возвращает объект `Response` в стиле разбивки на страницы для заданных выходных данных. """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class UserAnswerCreateAPIView(generics.CreateAPIView):
    """ Сохранение пользовательского ответа на вопрос """

    model = UserAnswer
    serializer_class = UserAnswerSerializer_Setter

    def perform_create(self, serializer):
        """
        Переопределение метода сохранения данных

        :param serializer: Сериализатор, указанный в serializer_class
        """

        serializer.save(user=self.request.user,  # Объект текущего пользователя
                        questionary=Questionary.objects.filter(pk=self.request.data.get("questionary")).first(),  # Объект текущего вопросника
                        answer=Answer.objects.filter(pk=self.request.data.get("answer")).first())  # Объект выбранного пользователем ответа


class ResultsAPIView(views.APIView):
    """ Отображение результата прохождения тестов """

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        """
        Переопределение метода получения

        :param request: Забираем текущего пользователя
        :param kwargs: Забираем идентификатор Вопросника
        """

        uanswer = UserAnswer.objects.prefetch_related('answer')\
            .filter(questionary__pk=kwargs['questionary_id'],
                    user__username=self.request.user)
        serializer = UserAnswerSerializer_Getter(uanswer, many=True)
        return response.Response(serializer.data)
