""" Представления """

from rest_framework import generics, viewsets, views, response
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Question, Questionary
from .paginations import QuestionAPIPagination
from .serializers import QuestionarySerializer, QuestionSerializer


class QuestionaryAPIView(generics.ListAPIView):
    queryset = Questionary.objects.all()
    serializer_class = QuestionarySerializer


class QuestionAPIView(views.APIView):
    pagination_class = QuestionAPIPagination
    authentication_classes = (TokenAuthentication,)  # authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = (IsAuthenticated,)  # permission_classes = [IsAuthenticated, ]
    # api_view = ['GET', 'POST']

    def get(self, request, format=None, **kwargs):
        question = Question.objects.filter(questionary__pk=kwargs['questionary_id'])
        page = self.paginate_queryset(question)
        if page is not None:
            serializer = QuestionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # serializer = QuestionSerializer(QuestionAPIPagination().paginate_queryset(question, request=request), many=True)
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

# class RandomQuestionAPIView(views.APIView):
#     def get(self, request, format=None, **kwargs):
#         question = Question.objects.filter(questionary__pk=kwargs['questionary_id']).order_by('?')[:1]
#         serializer = RandomQuestionSerializer(question, many=True)
#         return response.Response(serializer.data)

# class QuestionaryViewSet(viewsets.ReadOnlyModelViewSet):  # class QuestionaryAPIView(generics.ListAPIView):
#     # queryset = Questionary.objects.all()
#     serializer_class = QuestionarySerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Questionary.objects.all()
#
#         return Questionary.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def question(self, request, pk=None):
#         question = Question.objects.get(pk=pk)
#         return Response({'question_id': question.pk, 'question_text': question.text})
#
#     @action(methods=['get'], detail=False)
#     def questions(self, request):
#         questions = Question.objects.all()
#         return Response({'questions': [q.text for q in questions]})
#
#
# class QuestionAPIView(generics.ListAPIView):
#     pagination_class = QuestionAPIPagination
#     pass
#
#
# class AnswerRetrieveUpdAPIView(generics.RetrieveUpdateAPIView):
#     """ Чтение и изменение отдельного записи. GET- и POST-запросы. """
#     pass
